import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';
import 'reminders_screen.dart';
import 'emergency_sos_screen.dart';
import 'drug_info_screen.dart';
import 'nearby_hospitals_screen.dart';

class PatientDashboard extends StatefulWidget {
  const PatientDashboard({Key? key}) : super(key: key);

  @override
  State<PatientDashboard> createState() => _PatientDashboardState();
}

class _PatientDashboardState extends State<PatientDashboard> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('MediChain'),
        backgroundColor: Colors.blue,
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              Provider.of<AuthService>(context, listen: false).logout();
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(15),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Welcome message
            Consumer<AuthService>(
              builder: (context, authService, _) {
                return Text(
                  'Welcome, ${authService.userName}!',
                  style: const TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                );
              },
            ),
            const SizedBox(height: 20),
            // Feature grid
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              mainAxisSpacing: 15,
              crossAxisSpacing: 15,
              children: [
                _buildFeatureCard(
                  icon: Icons.medication,
                  title: 'Reminders',
                  subtitle: 'Medicine reminders',
                  color: Colors.pink,
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const RemindersScreen()),
                    );
                  },
                ),
                _buildFeatureCard(
                  icon: Icons.emergency,
                  title: 'Emergency SOS',
                  subtitle: 'Alert family',
                  color: Colors.red,
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const EmergencySosScreen()),
                    );
                  },
                ),
                _buildFeatureCard(
                  icon: Icons.warning,
                  title: 'Drug Info',
                  subtitle: 'Side effects',
                  color: Colors.orange,
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const DrugInfoScreen()),
                    );
                  },
                ),
                _buildFeatureCard(
                  icon: Icons.local_hospital,
                  title: 'Hospitals',
                  subtitle: 'Nearby hospitals',
                  color: Colors.green,
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const NearbyHospitalsScreen()),
                    );
                  },
                ),
                _buildFeatureCard(
                  icon: Icons.favorite,
                  title: 'Health Tracking',
                  subtitle: 'BP, Sugar, Weight',
                  color: Colors.purple,
                  onTap: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Health Tracking - Coming Soon')),
                    );
                  },
                ),
                _buildFeatureCard(
                  icon: Icons.message,
                  title: 'Messages',
                  subtitle: 'Chat with doctor',
                  color: Colors.blue,
                  onTap: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Messages - Coming Soon')),
                    );
                  },
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFeatureCard({
    required IconData icon,
    required String title,
    required String subtitle,
    required Color color,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [color.withOpacity(0.7), color],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(15),
          boxShadow: [
            BoxShadow(
              color: color.withOpacity(0.3),
              blurRadius: 8,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 40, color: Colors.white),
            const SizedBox(height: 10),
            Text(
              title,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 5),
            Text(
              subtitle,
              style: const TextStyle(
                fontSize: 12,
                color: Colors.white70,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
