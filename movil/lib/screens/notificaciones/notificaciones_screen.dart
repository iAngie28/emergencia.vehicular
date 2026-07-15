import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../providers/notificacion_provider.dart';
import '../../theme/colors.dart';
import '../servicios/reporte_respuesta_screen.dart';
import 'package:intl/intl.dart';

class NotificacionesScreen extends StatefulWidget {
  const NotificacionesScreen({super.key});

  @override
  State<NotificacionesScreen> createState() => _NotificacionesScreenState();
}

class _NotificacionesScreenState extends State<NotificacionesScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      _cargarNotificaciones();
    });
  }

  Future<void> _cargarNotificaciones() async {
    final userId = context.read<AuthProvider>().userId;
    if (userId != null) {
      await context.read<NotificacionProvider>().cargarHistorialNotificaciones(
        usuarioId: userId,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notificaciones'),
        backgroundColor: AppColors.primaryColor,
      ),
      body: Consumer<NotificacionProvider>(
        builder: (context, notificacionProvider, child) {
          if (notificacionProvider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          final notificaciones = notificacionProvider.notificacionesNoLeidas;

          if (notificaciones.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.notifications_none,
                    size: 64,
                    color: Colors.grey[400],
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'No tienes notificaciones',
                    style: Theme.of(context).textTheme.bodyLarge,
                  ),
                ],
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: _cargarNotificaciones,
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: notificaciones.length,
              itemBuilder: (context, index) {
                final notificacion = notificaciones[index];
                final esNoLeida = notificacion['leido'] != true;
                final fechaTexto =
                    notificacion['fecha_envio'] ??
                    notificacion['fecha_creacion'];
                final fecha = DateTime.tryParse(fechaTexto?.toString() ?? '');

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  color: esNoLeida
                      ? AppColors.info.withValues(alpha: 0.1)
                      : Colors.white,
                  child: ListTile(
                    contentPadding: const EdgeInsets.all(16),
                    leading: CircleAvatar(
                      backgroundColor: _getColorParaTipo(
                        notificacion['tipo_evento'] ?? '',
                      ),
                      child: Icon(
                        _getIconParaTipo(notificacion['tipo_evento'] ?? ''),
                        color: Colors.white,
                      ),
                    ),
                    title: Text(
                      notificacion['titulo'] ?? 'Notificación',
                      style: TextStyle(
                        fontWeight: esNoLeida
                            ? FontWeight.bold
                            : FontWeight.normal,
                      ),
                    ),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const SizedBox(height: 4),
                        Text(notificacion['mensaje'] ?? ''),
                        const SizedBox(height: 8),
                        if (fecha != null)
                          Text(
                            DateFormat('dd/MM/yyyy HH:mm').format(fecha),
                            style: const TextStyle(
                              fontSize: 12,
                              color: Colors.grey,
                            ),
                          ),
                      ],
                    ),
                    onTap: () => _abrirNotificacion(notificacion),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }

  Future<void> _abrirNotificacion(Map<String, dynamic> notificacion) async {
    final esNoLeida = notificacion['leido'] != true;
    final userId = context.read<AuthProvider>().userId;

    if (esNoLeida && notificacion['id'] != null) {
      await context.read<NotificacionProvider>().marcarComoLeida(
        notificacionId: _readInt(notificacion['id']) ?? 0,
        usuarioId: userId ?? 0,
      );
      notificacion['leido'] = true;
    }

    if (!mounted) return;

    final tipo = (notificacion['tipo'] ?? notificacion['tipo_evento'] ?? '')
        .toString()
        .toLowerCase();
    final incidenteId = _readInt(notificacion['incidente_id']);

    if (tipo == 'reporte_respondido' && incidenteId != null) {
      Navigator.of(context).push(
        MaterialPageRoute(
          builder: (_) => ReporteRespuestaScreen(incidenteId: incidenteId),
        ),
      );
      return;
    }

    _mostrarDetalleNotificacion(notificacion);
  }

  void _mostrarDetalleNotificacion(Map<String, dynamic> notificacion) {
    final fechaTexto =
        notificacion['fecha_envio'] ?? notificacion['fecha_creacion'];
    final fecha = DateTime.tryParse(fechaTexto?.toString() ?? '');

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(notificacion['titulo']?.toString() ?? 'Notificación'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(notificacion['mensaje']?.toString() ?? ''),
            if (notificacion['incidente_id'] != null) ...[
              const SizedBox(height: 12),
              Text('Incidente #${notificacion['incidente_id']}'),
            ],
            if (fecha != null) ...[
              const SizedBox(height: 12),
              Text(
                DateFormat('dd/MM/yyyy HH:mm').format(fecha.toLocal()),
                style: const TextStyle(fontSize: 12, color: Colors.grey),
              ),
            ],
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cerrar'),
          ),
        ],
      ),
    );
  }

  int? _readInt(dynamic value) {
    if (value is int) return value;
    return int.tryParse(value?.toString() ?? '');
  }

  Color _getColorParaTipo(String tipo) {
    switch (tipo.toLowerCase()) {
      case 'reporte_respondido':
        return AppColors.success;
      case 'incidente_aceptado':
        return AppColors.success;
      case 'llegada_taller':
        return AppColors.info;
      case 'pago_generado':
        return Colors.green;
      case 'oferta_recibida':
        return Colors.amber.shade700;
      default:
        return AppColors.secondaryColor;
    }
  }

  IconData _getIconParaTipo(String tipo) {
    switch (tipo.toLowerCase()) {
      case 'reporte_respondido':
        return Icons.mark_chat_read_outlined;
      case 'incidente_aceptado':
        return Icons.check_circle_outline;
      case 'llegada_taller':
        return Icons.build_circle_outlined;
      case 'pago_generado':
        return Icons.payment;
      case 'oferta_recibida':
        return Icons.local_offer_outlined;
      default:
        return Icons.notifications_active;
    }
  }
}
