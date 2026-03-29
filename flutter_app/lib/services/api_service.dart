import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'http://localhost:5000';

  // Login endpoint
  Future<Map<String, dynamic>> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/login'),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: {
          'username': username,
          'password': password,
        },
      );

      if (response.statusCode == 200) {
        // Parse response - for now return mock success
        return {
          'success': true,
          'role': 'patient',
          'name': username,
        };
      }
      return {'success': false};
    } catch (e) {
      print('API Error: $e');
      return {'success': false};
    }
  }

  // Register endpoint
  Future<Map<String, dynamic>> register(Map<String, dynamic> userData) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(userData),
      );

      if (response.statusCode == 200) {
        return {'success': true};
      }
      return {'success': false};
    } catch (e) {
      print('API Error: $e');
      return {'success': false};
    }
  }

  // Get patient data
  Future<Map<String, dynamic>> getPatientData(String patientId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/patient/$patientId'),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return {'success': false};
    } catch (e) {
      print('API Error: $e');
      return {'success': false};
    }
  }

  // Get reminders
  Future<List<dynamic>> getReminders(String patientId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/patient/$patientId/reminders'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['reminders'] ?? [];
      }
      return [];
    } catch (e) {
      print('API Error: $e');
      return [];
    }
  }

  // Mark medicine as taken
  Future<bool> markMedicineTaken(String reminderId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/mark-medicine-taken'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'reminder_id': reminderId}),
      );

      return response.statusCode == 200;
    } catch (e) {
      print('API Error: $e');
      return false;
    }
  }

  // Trigger SOS
  Future<bool> triggerSOS(String location, String message) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/trigger-sos'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'location': location,
          'message': message,
        }),
      );

      return response.statusCode == 200;
    } catch (e) {
      print('API Error: $e');
      return false;
    }
  }

  // Get nearby hospitals
  Future<List<dynamic>> getNearbyHospitals() async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/get-nearby-hospitals'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['hospitals'] ?? [];
      }
      return [];
    } catch (e) {
      print('API Error: $e');
      return [];
    }
  }

  // Get drug info
  Future<Map<String, dynamic>> getDrugInfo(String drugName) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/get-drug-info'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'drug_name': drugName}),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return {'success': false};
    } catch (e) {
      print('API Error: $e');
      return {'success': false};
    }
  }
}
