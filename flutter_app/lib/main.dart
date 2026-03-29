import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'screens/login_screen.dart';
import 'screens/patient_dashboard.dart';
import 'services/auth_service.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthService()),
      ],
      child: MaterialApp(
        title: 'MediChain',
        theme: ThemeData(
          primarySwatch: Colors.blue,
          useMaterial3: true,
          fontFamily: 'Poppins',
        ),
        home: const AuthWrapper(),
      ),
    );
  }
}

class AuthWrapper extends StatelessWidget {
  const AuthWrapper({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Consumer<AuthService>(
      builder: (context, authService, _) {
        if (authService.isLoggedIn) {
          return const PatientDashboard();
        } else {
          return const LoginScreen();
        }
      },
    );
  }
}
