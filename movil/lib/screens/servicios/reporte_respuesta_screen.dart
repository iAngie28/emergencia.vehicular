import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

import '../../services/api_service.dart';
import '../../theme/colors.dart';

class ReporteRespuestaScreen extends StatefulWidget {
  final int incidenteId;

  const ReporteRespuestaScreen({super.key, required this.incidenteId});

  @override
  State<ReporteRespuestaScreen> createState() => _ReporteRespuestaScreenState();
}

class _ReporteRespuestaScreenState extends State<ReporteRespuestaScreen> {
  Map<String, dynamic>? _reporte;
  String? _errorMessage;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      _cargarReporte();
    });
  }

  Future<void> _cargarReporte() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final response = await context.read<ApiService>().get(
        '/api/v1/reportes/incidente/${widget.incidenteId}/mi-reporte',
      );

      if (!mounted) return;
      if (response is Map<String, dynamic>) {
        setState(() {
          _reporte = response;
          _isLoading = false;
        });
      } else {
        setState(() {
          _errorMessage = 'El servidor devolvió una respuesta inesperada.';
          _isLoading = false;
        });
      }
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Respuesta del reporte'),
        backgroundColor: AppColors.primaryColor,
      ),
      body: _buildBody(context),
    );
  }

  Widget _buildBody(BuildContext context) {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_errorMessage != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.error_outline, color: AppColors.error, size: 48),
              const SizedBox(height: 12),
              Text(_errorMessage!, textAlign: TextAlign.center),
              const SizedBox(height: 16),
              ElevatedButton.icon(
                onPressed: _cargarReporte,
                icon: const Icon(Icons.refresh),
                label: const Text('Reintentar'),
              ),
            ],
          ),
        ),
      );
    }

    final reporte = _reporte;
    if (reporte == null) {
      return const Center(child: Text('No se encontró el reporte.'));
    }

    final estado = _text(reporte['estado']) ?? 'abierto';
    final tipo = _text(reporte['tipo_reporte']) == 'tecnico'
        ? 'Técnico'
        : 'Taller';
    final respuesta = _text(reporte['respuesta']);
    final tallerReportado = _text(reporte['taller_nombre']) ??
        _fallbackId(reporte['taller_id'], 'Taller no disponible');
    final tecnicoAsignado = _text(reporte['tecnico_nombre']) ??
        _fallbackId(reporte['tecnico_id'], 'Técnico no disponible');

    return RefreshIndicator(
      onRefresh: _cargarReporte,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const CircleAvatar(
                        backgroundColor: AppColors.primaryColor,
                        child: Icon(
                          Icons.mark_chat_read_outlined,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Reporte #${reporte['id']}',
                              style: Theme.of(context).textTheme.titleLarge,
                            ),
                            const SizedBox(height: 4),
                            Text('Incidente #${widget.incidenteId}'),
                          ],
                        ),
                      ),
                      _estadoChip(estado),
                    ],
                  ),
                  const SizedBox(height: 16),
                  _detalle('Tipo de reporte', tipo),
                  _detalle('Taller reportado', tallerReportado),
                  if (_text(reporte['tipo_reporte']) == 'tecnico')
                    _detalle('Técnico asignado', tecnicoAsignado),
                  _detalle('Motivo', _text(reporte['motivo']) ?? 'Sin motivo'),
                  _detalle(
                    'Fecha de creación',
                    _formatDate(reporte['fecha_creacion']),
                  ),
                  if (_text(reporte['fecha_resolucion']) != null)
                    _detalle(
                      'Fecha de respuesta',
                      _formatDate(reporte['fecha_resolucion']),
                    ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Tu reporte',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 8),
                  Text(_text(reporte['descripcion']) ?? 'Sin descripción.'),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        respuesta == null
                            ? Icons.hourglass_empty
                            : Icons.reply_all_outlined,
                        color: respuesta == null
                            ? AppColors.textLight
                            : AppColors.success,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        'Respuesta',
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Text(
                    respuesta ?? 'Aún no hay respuesta registrada.',
                    style: const TextStyle(height: 1.35),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _detalle(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(top: 10),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 125,
            child: Text(
              label,
              style: const TextStyle(
                color: AppColors.textLight,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
          Expanded(child: Text(value)),
        ],
      ),
    );
  }

  Widget _estadoChip(String estado) {
    final color = switch (estado.toLowerCase()) {
      'resuelto' => AppColors.success,
      'en_revision' => AppColors.warning,
      _ => AppColors.info,
    };

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(
        estado.toUpperCase(),
        style: TextStyle(
          color: color,
          fontSize: 11,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }

  String _formatDate(dynamic value) {
    final text = _text(value);
    if (text == null) return 'No disponible';

    final date = DateTime.tryParse(text);
    if (date == null) return text;

    return DateFormat('dd/MM/yyyy HH:mm').format(date.toLocal());
  }

  String? _text(dynamic value) {
    if (value == null) return null;
    final text = value.toString().trim();
    return text.isEmpty ? null : text;
  }

  String _fallbackId(dynamic value, String fallback) {
    final text = _text(value);
    return text == null ? fallback : '#$text';
  }
}
