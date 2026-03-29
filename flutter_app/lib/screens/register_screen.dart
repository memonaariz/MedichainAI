import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({Key? key}) : super(key: key);

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _ageController = TextEditingController();
  final _phoneController = TextEditingController();
  final _emailController = TextEditingController();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();

  String? _selectedBloodGroup;
  List<String> _selectedAllergies = [];
  List<String> _selectedMedicalHistory = [];

  final List<String> bloodGroups = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'];
  final List<String> allergies = ['Penicillin', 'Aspirin', 'Ibuprofen', 'Shellfish', 'Peanuts'];
  final List<String> medicalHistory = ['Diabetes', 'Hypertension', 'Heart Disease', 'Asthma', 'Thyroid'];

  @override
  void dispose() {
    _nameController.dispose();
    _ageController.dispose();
    _phoneController.dispose();
    _emailController.dispose();
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _register() async {
    if (_formKey.currentState!.validate()) {
      final authService = Provider.of<AuthService>(context, listen: false);
      
      final userData = {
        'full_name': _nameController.text,
        'age': _ageController.text,
        'phone': _phoneController.text,
        'email': _emailController.text,
        'blood_group': _selectedBloodGroup,
        'allergies': _selectedAllergies,
        'medical_history': _selectedMedicalHistory,
        'username': _usernameController.text,
        'password': _passwordController.text,
      };

      final success = await authService.register(userData);

      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('✓ Registration successful! Please login.')),
        );
        Navigator.pop(context);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('❌ Registration failed')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Register'),
        backgroundColor: Colors.blue,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              // Basic Info
              TextFormField(
                controller: _nameController,
                decoration: InputDecoration(
                  labelText: 'Full Name',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                ),
                validator: (value) => value?.isEmpty ?? true ? 'Required' : null,
              ),
              const SizedBox(height: 15),
              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: _ageController,
                      keyboardType: TextInputType.number,
                      decoration: InputDecoration(
                        labelText: 'Age',
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                      validator: (value) => value?.isEmpty ?? true ? 'Required' : null,
                    ),
                  ),
                  const SizedBox(width: 15),
                  Expanded(
                    child: DropdownButtonFormField<String>(
                      value: _selectedBloodGroup,
                      decoration: InputDecoration(
                        labelText: 'Blood Group',
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                      items: bloodGroups.map((bg) => DropdownMenuItem(value: bg, child: Text(bg))).toList(),
                      onChanged: (value) => setState(() => _selectedBloodGroup = value),
                      validator: (value) => value == null ? 'Required' : null,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 15),
              TextFormField(
                controller: _phoneController,
                keyboardType: TextInputType.phone,
                decoration: InputDecoration(
                  labelText: 'Phone',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                ),
                validator: (value) => value?.isEmpty ?? true ? 'Required' : null,
              ),
              const SizedBox(height: 15),
              TextFormField(
                controller: _emailController,
                keyboardType: TextInputType.emailAddress,
                decoration: InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                ),
                validator: (value) => value?.isEmpty ?? true ? 'Required' : null,
              ),
              const SizedBox(height: 20),
              // Allergies
              const Align(
                alignment: Alignment.centerLeft,
                child: Text('Allergies:', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
              const SizedBox(height: 10),
              Wrap(
                spacing: 10,
                children: allergies.map((allergy) {
                  return FilterChip(
                    label: Text(allergy),
                    selected: _selectedAllergies.contains(allergy),
                    onSelected: (selected) {
                      setState(() {
                        if (selected) {
                          _selectedAllergies.add(allergy);
                        } else {
                          _selectedAllergies.remove(allergy);
                        }
                      });
                    },
                  );
                }).toList(),
              ),
              const SizedBox(height: 20),
              // Medical History
              const Align(
                alignment: Alignment.centerLeft,
                child: Text('Medical History:', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
              const SizedBox(height: 10),
              Wrap(
                spacing: 10,
                children: medicalHistory.map((condition) {
                  return FilterChip(
                    label: Text(condition),
                    selected: _selectedMedicalHistory.contains(condition),
                    onSelected: (selected) {
                      setState(() {
                        if (selected) {
                          _selectedMedicalHistory.add(condition);
                        } else {
                          _selectedMedicalHistory.remove(condition);
                        }
                      });
                    },
                  );
                }).toList(),
              ),
              const SizedBox(height: 20),
              // Account Info
              TextFormField(
                controller: _usernameController,
                decoration: InputDecoration(
                  labelText: 'Username',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                ),
                validator: (value) => value?.isEmpty ?? true ? 'Required' : null,
              ),
              const SizedBox(height: 15),
              TextFormField(
                controller: _passwordController,
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                ),
                validator: (value) => value?.isEmpty ?? true ? 'Required' : null,
              ),
              const SizedBox(height: 25),
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: _register,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                  child: const Text(
                    'Register',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white),
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
