// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../services/api_service.dart';
import '../../theme/colors.dart';

class ReporteScreen extends StatefulWidget {
  final int incidenteId;
  final int? tecnicoId;

  const ReporteScreen({super.key, required this.incidenteId, this.tecnicoId});

  @override
  State<ReporteScreen> createState() => _ReporteScreenState();
}

class _ReporteScreenState extends State<ReporteScreen> {
  final _formKey = GlobalKey<FormState>();
  String _tipoReporte = 'taller'; // 'taller' o 'tecnico'
  final TextEditingController _motivoController = TextEditingController();
  final TextEditingController _descripcionController = TextEditingController();
  bool _isSubmitting = false;

  @override
  void initState() {
    super.initState();
    _tipoReporte = widget.tecnicoId != null ? 'tecnico' : 'taller';
  }

  @override
  void dispose() {
    _motivoController.dispose();
    _descripcionController.dispose();
    super.dispose();
  }

  Future<void> _enviarReporte() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isSubmitting = true;
    });

    final apiService = context.read<ApiService>();
    final payload = {
      'incidente_id': widget.incidenteId,
      'tipo_reporte': _tipoReporte,
      'motivo': _motivoController.text.trim(),
      'descripcion': _descripcionController.text.trim(),
      'tecnico_id': _tipoReporte == 'tecnico' ? widget.tecnicoId : null,
    };

    try {
      await apiService.post('/api/v1/reportes/', body: payload);
      if (!mounted) return;

      showDialog(
        context: context,
        builder: (ctx) => AlertDialog(
          title: const Text('Reporte Registrado'),
          content: const Text(
            'Tu reporte ha sido enviado y será auditado por el equipo de calidad.',
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(ctx).pop(); // Cerrar dialog
                Navigator.of(context).pop(); // Volver atrás
              },
              child: const Text('Aceptar'),
            ),
          ],
        ),
      );
    } catch (e) {
      setState(() {
        _isSubmitting = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Error al enviar reporte (solo se permite un reporte por taller y uno por tecnico en cada incidente): $e',
          ),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final tieneTecnico = widget.tecnicoId != null;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Crear Reporte de Calidad'),
        backgroundColor: AppColors.primaryColor,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Seleccione el tipo de reporte:',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),

              // Selector de Taller / Técnico
              Row(
                children: [
                  Radio<String>(
                    value: 'taller',
                    groupValue: _tipoReporte,
                    onChanged: (val) {
                      if (val != null) {
                        setState(() {
                          _tipoReporte = val;
                        });
                      }
                    },
                  ),
                  const Text('Reportar Taller (Ir al Superadmin)'),
                ],
              ),
              if (tieneTecnico)
                Row(
                  children: [
                    Radio<String>(
                      value: 'tecnico',
                      groupValue: _tipoReporte,
                      onChanged: (val) {
                        if (val != null) {
                          setState(() {
                            _tipoReporte = val;
                          });
                        }
                      },
                    ),
                    const Text(
                      'Reportar Técnico (Ir al Administrador de Taller)',
                    ),
                  ],
                ),
              const SizedBox(height: 16),

              // Motivo
              TextFormField(
                controller: _motivoController,
                decoration: const InputDecoration(
                  labelText: 'Motivo abreviado',
                  hintText:
                      'Ej: Demora excesiva, Maltrato, Falta de herramientas',
                  border: OutlineInputBorder(),
                ),
                validator: (val) {
                  if (val == null || val.trim().isEmpty) {
                    return 'Por favor escribe el motivo del reporte';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Descripción
              TextFormField(
                controller: _descripcionController,
                decoration: const InputDecoration(
                  labelText: 'Descripción detallada de la queja',
                  alignLabelWithHint: true,
                  border: OutlineInputBorder(),
                ),
                maxLines: 5,
                validator: (val) {
                  if (val == null || val.trim().isEmpty) {
                    return 'Por favor explica a detalle lo ocurrido';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),

              // Botón de Enviar
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _isSubmitting ? null : _enviarReporte,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primaryColor,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: _isSubmitting
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            color: Colors.white,
                            strokeWidth: 2,
                          ),
                        )
                      : const Text(
                          'Enviar Reporte',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
