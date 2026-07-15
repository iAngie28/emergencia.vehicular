import 'dart:convert';

import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import '../main.dart';
import '../screens/notificaciones/notificaciones_screen.dart';
import '../screens/pagos/pagos_screen.dart';
import '../screens/servicios/reporte_respuesta_screen.dart';
import 'package:flutter/material.dart';

class LocalNotificationService {
  static final LocalNotificationService _instance =
      LocalNotificationService._internal();

  factory LocalNotificationService() {
    return _instance;
  }

  LocalNotificationService._internal();

  final FlutterLocalNotificationsPlugin _flutterLocalNotificationsPlugin =
      FlutterLocalNotificationsPlugin();
  bool _isInitialized = false;

  Future<void> initialize() async {
    if (_isInitialized) return;

    const AndroidInitializationSettings initializationSettingsAndroid =
        AndroidInitializationSettings('@mipmap/ic_launcher');

    const InitializationSettings initializationSettings =
        InitializationSettings(android: initializationSettingsAndroid);

    await _flutterLocalNotificationsPlugin.initialize(
      initializationSettings,
      onDidReceiveNotificationResponse: (NotificationResponse response) {
        handleNotificationPayload(response.payload);
      },
    );

    // Request permissions for Android 13+
    _flutterLocalNotificationsPlugin
        .resolvePlatformSpecificImplementation<
          AndroidFlutterLocalNotificationsPlugin
        >()
        ?.requestNotificationsPermission();

    _isInitialized = true;
  }

  Future<void> showNotification({
    required int id,
    required String title,
    required String body,
    String? payload,
  }) async {
    if (!_isInitialized) await initialize();

    const AndroidNotificationDetails androidPlatformChannelSpecifics =
        AndroidNotificationDetails(
          'emergencia_vehicular_channel_id',
          'Notificaciones de Emergencia',
          channelDescription:
              'Canal para notificaciones de auxilios e incidentes',
          importance: Importance.max,
          priority: Priority.high,
          showWhen: true,
          icon: '@mipmap/ic_launcher',
        );
    const NotificationDetails platformChannelSpecifics = NotificationDetails(
      android: androidPlatformChannelSpecifics,
    );

    await _flutterLocalNotificationsPlugin.show(
      id,
      title,
      body,
      platformChannelSpecifics,
      payload: payload,
    );
  }

  static String payloadForData(Map<String, dynamic> data) {
    return jsonEncode(
      data.map((key, value) => MapEntry(key, value?.toString() ?? '')),
    );
  }

  void handleNotificationData(Map<String, dynamic> data) {
    final tipo = (data['tipo'] ?? data['evento'] ?? '')
        .toString()
        .toLowerCase();
    final incidenteId = _readInt(data['incidente_id']);

    if (tipo == 'reporte_respondido' && incidenteId != null) {
      _pushScreen(ReporteRespuestaScreen(incidenteId: incidenteId));
      return;
    }

    if (tipo == 'cobro_generado' ||
        tipo == 'pago_generado' ||
        data['evento'] == 'cobro_generado') {
      _pushScreen(const PagosScreen(initialIndex: 1));
      return;
    }

    _pushScreen(const NotificacionesScreen());
  }

  void handleNotificationPayload(String? payload) {
    if (payload == null || payload.isEmpty) {
      _pushScreen(const NotificacionesScreen());
      return;
    }

    if (payload == 'pago') {
      _pushScreen(const PagosScreen(initialIndex: 1));
      return;
    }

    try {
      final decoded = jsonDecode(payload);
      if (decoded is Map<String, dynamic>) {
        handleNotificationData(decoded);
        return;
      }
    } catch (_) {
      final incidenteId = _readInt(payload);
      if (incidenteId != null) {
        _pushScreen(const NotificacionesScreen());
        return;
      }
    }

    _pushScreen(const NotificacionesScreen());
  }

  void _pushScreen(Widget screen) {
    final navigator = navigatorKey.currentState;
    if (navigator == null) {
      Future.delayed(
        const Duration(milliseconds: 400),
        () => _pushScreen(screen),
      );
      return;
    }

    navigator.push(MaterialPageRoute(builder: (_) => screen));
  }

  int? _readInt(dynamic value) {
    if (value is int) return value;
    return int.tryParse(value?.toString() ?? '');
  }
}
