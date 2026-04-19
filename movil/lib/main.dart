import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

// Servicios
import 'services/api_service.dart';
import 'services/auth_service.dart';
import 'services/incidente_service.dart';
import 'services/vehiculo_service.dart';
import 'services/pago_service.dart';
import 'services/notificacion_service.dart';
import 'services/usuario_service.dart';
import 'services/taller_service.dart';

// Providers
import 'providers/auth_provider.dart';
import 'providers/incidente_provider.dart';
import 'providers/vehiculo_provider.dart';
import 'providers/pago_provider.dart';
import 'providers/notificacion_provider.dart';
import 'providers/usuario_provider.dart';

// Pantallas
import 'theme/colors.dart';
import 'screens/incidentes/reportar_incidente_screen.dart';
import 'screens/incidentes/mis_incidentes_screen.dart';
import 'screens/vehiculos/mis_vehiculos_screen.dart';
import 'screens/pagos/pagos_screen.dart';
import 'screens/perfil/perfil_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // URL del backend - IMPORTANTE: Cambiar según tu configuración
    // En desarrollo local, cambiar por: http://localhost:5000
    // Para pruebas en teléfono, usar la IP local: http://192.168.X.X:5000
    const String backendUrl = 'http://192.168.0.50:5000';
    
    return MultiProvider(
      providers: [
        // ApiService base
        Provider<ApiService>(
          create: (_) => ApiService(baseUrl: backendUrl),
        ),

        // Servicios
        Provider<AuthService>(
          create: (context) => AuthService(
            apiService: context.read<ApiService>(),
          ),
        ),
        Provider<IncidenteService>(
          create: (context) => IncidenteService(
            apiService: context.read<ApiService>(),
          ),
        ),
        Provider<VehiculoService>(
          create: (context) => VehiculoService(
            apiService: context.read<ApiService>(),
          ),
        ),
        Provider<PagoService>(
          create: (context) => PagoService(
            apiService: context.read<ApiService>(),
          ),
        ),
        Provider<NotificacionService>(
          create: (context) => NotificacionService(
            apiService: context.read<ApiService>(),
          ),
        ),
        Provider<UsuarioService>(
          create: (context) => UsuarioService(
            apiService: context.read<ApiService>(),
          ),
        ),
        Provider<TallerService>(
          create: (context) => TallerService(
            apiService: context.read<ApiService>(),
          ),
        ),

        // Providers (estado global)
        ChangeNotifierProvider(
          create: (context) => AuthProvider(
            authService: context.read<AuthService>(),
          ),
        ),
        ChangeNotifierProvider(
          create: (context) => IncidenteProvider(
            incidenteService: context.read<IncidenteService>(),
          ),
        ),
        ChangeNotifierProvider(
          create: (context) => VehiculoProvider(
            vehiculoService: context.read<VehiculoService>(),
          ),
        ),
        ChangeNotifierProvider(
          create: (context) => PagoProvider(
            pagoService: context.read<PagoService>(),
          ),
        ),
        ChangeNotifierProvider(
          create: (context) => NotificacionProvider(
            notificacionService: context.read<NotificacionService>(),
          ),
        ),
        ChangeNotifierProvider(
          create: (context) => UsuarioProvider(
            usuarioService: context.read<UsuarioService>(),
          ),
        ),
      ],
      child: MaterialApp(
        title: 'Emergencia Vehicular',
        theme: appTheme,
        home: Consumer<AuthProvider>(
          builder: (context, authProvider, _) {
            return authProvider.isAuthenticated ? const HomePage() : const LoginPage();
          },
        ),
      ),
    );
  }
}

/// Pantalla de Login
class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  void _handleLogin(BuildContext context) async {
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Por favor completa todos los campos')),
      );
      return;
    }

    // Llamar a AuthProvider para conectar con backend
    final authProvider = context.read<AuthProvider>();
    final success = await authProvider.login(email, password);

    if (success) {
      // Navegar a HomePage
      if (mounted) {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (context) => const HomePage()),
        );
      }
    } else {
      // Mostrar error
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(authProvider.errorMessage ?? 'Error al iniciar sesión'),
            backgroundColor: AppColors.error,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.scaffoldBackground,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: SingleChildScrollView(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Logo/Título
                Text(
                  'Emergencia\nVehicular',
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.displayLarge?.copyWith(
                    fontSize: 32,
                    color: AppColors.primaryColor,
                  ),
                ),
                const SizedBox(height: 48),

                // Email
                TextField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  decoration: InputDecoration(
                    hintText: 'Correo electrónico',
                    prefixIcon: const Icon(Icons.email, color: AppColors.secondaryColor),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // Contraseña
                TextField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: InputDecoration(
                    hintText: 'Contraseña',
                    prefixIcon: const Icon(Icons.lock, color: AppColors.secondaryColor),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
                const SizedBox(height: 32),

                // Botón Login - Conectado con Backend
                Consumer<AuthProvider>(
                  builder: (context, authProvider, _) {
                    return SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: authProvider.isLoading ? null : () => _handleLogin(context),
                        child: authProvider.isLoading
                            ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            valueColor: AlwaysStoppedAnimation(Colors.white),
                          ),
                        )
                            : const Text('Iniciar Sesión', style: TextStyle(fontSize: 16)),
                      ),
                    );
                  },
                ),

                // Mensaje de error (si existe)
                Consumer<AuthProvider>(
                  builder: (context, authProvider, _) {
                    if (authProvider.errorMessage != null) {
                      return Padding(
                        padding: const EdgeInsets.only(top: 16),
                        child: Text(
                          authProvider.errorMessage!,
                          style: const TextStyle(color: AppColors.error),
                          textAlign: TextAlign.center,
                        ),
                      );
                    }
                    return const SizedBox.shrink();
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}

/// Pantalla Principal
class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Asistencia Vehicular'),
        backgroundColor: AppColors.primaryColor,
        elevation: 0,
      ),
      body: _buildPage(_selectedIndex),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        selectedItemColor: AppColors.primaryColor,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Inicio'),
          BottomNavigationBarItem(icon: Icon(Icons.history), label: 'Historial'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Perfil'),
        ],
      ),
    );
  }

  Widget _buildPage(int index) {
    switch (index) {
      case 0:
        return const HomePage_Dashboard();
      case 1:
        return const MisIncidentesScreen();
      case 2:
        return const PerfilScreen();
      default:
        return const HomePage_Dashboard();
    }
  }
}

/// Dashboard - Pantalla Principal
class HomePage_Dashboard extends StatelessWidget {
  const HomePage_Dashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Tarjeta de Estado
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.primaryColor,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Row(
              children: [
                const Icon(Icons.check_circle, color: Colors.white, size: 32),
                const SizedBox(width: 16),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Estado: Activo',
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    const Text(
                      'Listo para reportar incidentes',
                      style: TextStyle(color: Colors.white70),
                    ),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(height: 32),

          // Opciones principales
          Text(
            'Acciones Rápidas',
            style: Theme.of(context).textTheme.displayLarge?.copyWith(fontSize: 18),
          ),
          const SizedBox(height: 16),

          // Botón Reportar Incidente
          GestureDetector(
            onTap: () => Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => const ReportarIncidenteScreen(),
              ),
            ),
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.secondaryColor,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  const Icon(Icons.report_problem, color: Colors.white, size: 32),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Reportar Incidente',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                        ),
                        const SizedBox(height: 4),
                        const Text(
                          'Describe tu emergencia',
                          style: TextStyle(color: Colors.white70, fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                  const Icon(Icons.arrow_forward, color: Colors.white),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Botón Ver Vehículos
          GestureDetector(
            onTap: () => Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => const MisVehiculosScreen(),
              ),
            ),
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.accentColor,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  const Icon(Icons.directions_car, color: Colors.white, size: 32),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Mis Vehículos',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                        ),
                        const SizedBox(height: 4),
                        const Text(
                          'Gestiona tus vehículos',
                          style: TextStyle(color: Colors.white70, fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                  const Icon(Icons.arrow_forward, color: Colors.white),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Botón Ver Pagos
          GestureDetector(
            onTap: () => Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => const PagosScreen(),
              ),
            ),
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.purple,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  const Icon(Icons.receipt_long, color: Colors.white, size: 32),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Pagos y Facturas',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                        ),
                        const SizedBox(height: 4),
                        const Text(
                          'Historial de pagos y facturas',
                          style: TextStyle(color: Colors.white70, fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                  const Icon(Icons.arrow_forward, color: Colors.white),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
