import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'api_service.dart';

class AuthService extends ChangeNotifier {
  bool _isLoggedIn = false;
  String? _username;
  String? _userRole;
  String? _userName;

  bool get isLoggedIn => _isLoggedIn;
  String? get username => _username;
  String? get userRole => _userRole;
  String? get userName => _userName;

  final ApiService _apiService = ApiService();

  AuthService() {
    _checkLoginStatus();
  }

  Future<void> _checkLoginStatus() async {
    final prefs = await SharedPreferences.getInstance();
    _isLoggedIn = prefs.getBool('isLoggedIn') ?? false;
    _username = prefs.getString('username');
    _userRole = prefs.getString('userRole');
    _userName = prefs.getString('userName');
    notifyListeners();
  }

  Future<bool> login(String username, String password) async {
    try {
      final response = await _apiService.login(username, password);
      
      if (response['success']) {
        _isLoggedIn = true;
        _username = username;
        _userRole = response['role'];
        _userName = response['name'];

        final prefs = await SharedPreferences.getInstance();
        await prefs.setBool('isLoggedIn', true);
        await prefs.setString('username', username);
        await prefs.setString('userRole', _userRole ?? '');
        await prefs.setString('userName', _userName ?? '');

        notifyListeners();
        return true;
      }
      return false;
    } catch (e) {
      print('Login error: $e');
      return false;
    }
  }

  Future<bool> register(Map<String, dynamic> userData) async {
    try {
      final response = await _apiService.register(userData);
      return response['success'] ?? false;
    } catch (e) {
      print('Register error: $e');
      return false;
    }
  }

  Future<void> logout() async {
    _isLoggedIn = false;
    _username = null;
    _userRole = null;
    _userName = null;

    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    notifyListeners();
  }
}
