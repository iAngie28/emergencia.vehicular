import 'package:flutter/material.dart';

import '../../theme/colors.dart';

class SeguimientoScreen extends StatelessWidget {
  const SeguimientoScreen({super.key, required this.incidente});

  final Map<String, dynamic> incidente;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Seguimiento en Tiempo Real')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              gradient: const LinearGradient(
                colors: [Color(0xFF1D4ED8), Color(0xFF2563EB)],
              ),
            ),
            child: const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Diagnostico Inteligente',
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(height: 8),
                Text(
                  'Tipo de problema estimado: Falla mecanica',
                  style: TextStyle(color: Colors.white),
                ),
                Text(
                  'Prioridad estimada: ALTA',
                  style: TextStyle(color: Colors.white),
                ),
                Text(
                  'Estado IA: Maquetado',
                  style: TextStyle(color: Colors.white70),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Estado del Servicio',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Estado: ${(incidente['estado'] ?? 'pendiente').toString().toUpperCase()}',
                  ),
                  Text(
                    'Ubicacion: ${incidente['ubicacion'] ?? 'No especificada'}',
                  ),
                  const Text('Taller asignado: En espera de asignacion'),
                  const Text('ETA estimado: 10-20 min'),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          Container(
            height: 200,
            decoration: BoxDecoration(
              color: const Color(0xFFEFF6FF),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: const Color(0xFFBFDBFE)),
            ),
            child: const Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.map_outlined, size: 56, color: AppColors.info),
                  SizedBox(height: 8),
                  Text('Mapa en tiempo real (maquetado)'),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: ElevatedButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.chat),
                  label: const Text('WhatsApp'),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.phone),
                  label: const Text('Llamar'),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
