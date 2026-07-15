import 'dart:async';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../services/api_service.dart';
import '../../services/realtime_service.dart';
import '../../providers/auth_provider.dart';
import '../../theme/colors.dart';

class ChatScreen extends StatefulWidget {
  final int incidenteId;
  final String tallerNombre;

  const ChatScreen({
    super.key,
    required this.incidenteId,
    required this.tallerNombre,
  });

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<Map<String, dynamic>> _mensajes = [];
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  StreamSubscription? _realtimeSubscription;
  bool _isLoading = true;
  int? _userId;

  @override
  void initState() {
    super.initState();
    _userId = context.read<AuthProvider>().userId;
    _cargarHistorial();
    _suscribirRealtime();
  }

  @override
  void dispose() {
    _realtimeSubscription?.cancel();
    _messageController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _cargarHistorial() async {
    final apiService = context.read<ApiService>();
    try {
      final List<dynamic> response = await apiService.get(
        '/api/v1/incidentes/${widget.incidenteId}/chat',
      );
      if (!mounted) return;
      setState(() {
        _mensajes.clear();
        for (var item in response) {
          if (item is Map<String, dynamic>) {
            _mensajes.add(item);
          }
        }
        _isLoading = false;
      });
      _scrollToBottom();
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _isLoading = false;
      });
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Error al cargar historial: $e')));
    }
  }

  void _suscribirRealtime() {
    final realtimeService = context.read<RealtimeService>();
    _realtimeSubscription = realtimeService.events.listen((event) {
      if (event['tipo'] == 'chat_message' &&
          event['incidente_id'] == widget.incidenteId) {
        setState(() {
          _mensajes.add(event);
        });
        _scrollToBottom();
      }
    });
  }

  void _enviarMensaje() {
    final text = _messageController.text.trim();
    if (text.isEmpty) return;

    final realtimeService = context.read<RealtimeService>();
    final payload = {
      'tipo': 'chat_message',
      'incidente_id': widget.incidenteId,
      'contenido': text,
      'tipo_msg': 'texto',
    };

    realtimeService.send(payload);

    setState(() {
      _mensajes.add({
        'remitente_id': _userId,
        'contenido': text,
        'fecha_envio': DateTime.now().toUtc().toIso8601String(),
      });
      _messageController.clear();
    });
    _scrollToBottom();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Chat con Soporte',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            Text(
              widget.tallerNombre,
              style: const TextStyle(fontSize: 12, color: Colors.white70),
            ),
          ],
        ),
        backgroundColor: AppColors.primaryColor,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                Expanded(
                  child: _mensajes.isEmpty
                      ? const Center(
                          child: Text(
                            'No hay mensajes. ¡Escribe un mensaje para iniciar el chat!',
                            textAlign: TextAlign.center,
                            style: TextStyle(color: Colors.grey),
                          ),
                        )
                      : ListView.builder(
                          controller: _scrollController,
                          padding: const EdgeInsets.all(16),
                          itemCount: _mensajes.length,
                          itemBuilder: (context, index) {
                            final msg = _mensajes[index];
                            final isMe = msg['remitente_id'] == _userId;
                            return _buildMessageBubble(
                              msg['contenido'] ?? '',
                              isMe,
                            );
                          },
                        ),
                ),
                _buildInputBar(),
              ],
            ),
    );
  }

  Widget _buildMessageBubble(String text, bool isMe) {
    return Align(
      alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 8),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        decoration: BoxDecoration(
          color: isMe ? AppColors.primaryColor : Colors.grey[200],
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(12),
            topRight: const Radius.circular(12),
            bottomLeft: isMe
                ? const Radius.circular(12)
                : const Radius.circular(0),
            bottomRight: isMe
                ? const Radius.circular(0)
                : const Radius.circular(12),
          ),
        ),
        child: Text(
          text,
          style: TextStyle(
            color: isMe ? Colors.white : Colors.black87,
            fontSize: 15,
          ),
        ),
      ),
    );
  }

  Widget _buildInputBar() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
      color: Colors.white,
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _messageController,
              decoration: const InputDecoration(
                hintText: 'Escribe un mensaje...',
                border: InputBorder.none,
                contentPadding: EdgeInsets.symmetric(horizontal: 12),
              ),
              onSubmitted: (_) => _enviarMensaje(),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.send, color: AppColors.primaryColor),
            onPressed: _enviarMensaje,
          ),
        ],
      ),
    );
  }
}
