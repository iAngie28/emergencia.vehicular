import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../providers/auth_provider.dart';
import '../../providers/incidente_provider.dart';

class HistorialScreen extends StatefulWidget {
  const HistorialScreen({super.key});

  @override
  State<HistorialScreen> createState() => _HistorialScreenState();
}

class _HistorialScreenState extends State<HistorialScreen> {
  @override
  void initState() {
    super.initState();
    Future.microtask(_cargar);
  }

  Future<void> _cargar() async {
    final userId = context.read<AuthProvider>().userId;
    if (userId == null) return;
    await context.read<IncidenteProvider>().cargarMisIncidentes(
      usuarioId: userId,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<IncidenteProvider>(
      builder: (context, provider, _) {
        final historial = provider.misIncidentes.where((item) {
          final estado = (item['estado'] ?? '').toString().toLowerCase();
          return estado == 'atendido' ||
              estado == 'completado' ||
              estado == 'cancelado';
        }).toList();

        if (provider.isLoading) {
          return const Center(child: CircularProgressIndicator());
        }

        if (historial.isEmpty) {
          return const Center(child: Text('No hay servicios completados aun'));
        }

        return RefreshIndicator(
          onRefresh: _cargar,
          child: ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: historial.length,
            itemBuilder: (_, index) {
              final item = historial[index];
              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  title: Text(item['descripcion']?.toString() ?? 'Incidente'),
                  subtitle: Text(
                    item['ubicacion']?.toString() ?? 'Sin ubicacion',
                  ),
                  trailing: Text(
                    (item['estado'] ?? '').toString().toUpperCase(),
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
              );
            },
          ),
        );
      },
    );
  }
}
