import 'package:flutter/material.dart';

class DrugInfoScreen extends StatefulWidget {
  const DrugInfoScreen({Key? key}) : super(key: key);

  @override
  State<DrugInfoScreen> createState() => _DrugInfoScreenState();
}

class _DrugInfoScreenState extends State<DrugInfoScreen> {
  final _searchController = TextEditingController();
  Map<String, dynamic>? _drugInfo;
  bool _isLoading = false;

  final Map<String, Map<String, dynamic>> drugDatabase = {
    'amlong': {
      'name': 'Amlodipine (Amlong)',
      'type': 'Blood Pressure Medication',
      'common_side_effects': ['Swelling in feet/ankles', 'Headache', 'Dizziness', 'Fatigue'],
      'serious_side_effects': ['Chest pain', 'Severe dizziness', 'Fainting'],
      'severity': 'MEDIUM',
    },
    'metformin': {
      'name': 'Metformin',
      'type': 'Diabetes Medication',
      'common_side_effects': ['Nausea', 'Diarrhea', 'Stomach upset', 'Metallic taste'],
      'serious_side_effects': ['Lactic acidosis (rare)', 'Vitamin B12 deficiency'],
      'severity': 'MEDIUM',
    },
    'aspirin': {
      'name': 'Aspirin',
      'type': 'Pain Reliever / Blood Thinner',
      'common_side_effects': ['Stomach upset', 'Heartburn', 'Nausea'],
      'serious_side_effects': ['Bleeding', 'Allergic reaction', 'Asthma attack'],
      'severity': 'HIGH',
    },
  };

  void _searchDrug() {
    final drugName = _searchController.text.toLowerCase();
    setState(() => _isLoading = true);

    Future.delayed(const Duration(milliseconds: 500), () {
      setState(() {
        _drugInfo = drugDatabase[drugName];
        _isLoading = false;
      });

      if (_drugInfo == null) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Drug not found')),
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Drug Information'),
        backgroundColor: Colors.blue,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(15),
        child: Column(
          children: [
            // Search field
            TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: 'Search drug (e.g., Amlong, Metformin)',
                prefixIcon: const Icon(Icons.search),
                suffixIcon: IconButton(
                  icon: const Icon(Icons.clear),
                  onPressed: () {
                    _searchController.clear();
                    setState(() => _drugInfo = null);
                  },
                ),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
              onSubmitted: (_) => _searchDrug(),
            ),
            const SizedBox(height: 15),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _searchDrug,
                style: ElevatedButton.styleFrom(backgroundColor: Colors.blue),
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text('Search', style: TextStyle(color: Colors.white)),
              ),
            ),
            const SizedBox(height: 30),
            // Drug info display
            if (_drugInfo != null)
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    padding: const EdgeInsets.all(15),
                    decoration: BoxDecoration(
                      color: Colors.blue.shade50,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          _drugInfo!['name'],
                          style: const TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 5),
                        Text(
                          _drugInfo!['type'],
                          style: const TextStyle(color: Colors.grey),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 20),
                  const Text(
                    'Common Side Effects:',
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                  ),
                  const SizedBox(height: 10),
                  ..._drugInfo!['common_side_effects'].map<Widget>((effect) {
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 8),
                      child: Row(
                        children: [
                          const Icon(Icons.check_circle, color: Colors.green, size: 20),
                          const SizedBox(width: 10),
                          Expanded(child: Text(effect)),
                        ],
                      ),
                    );
                  }).toList(),
                  const SizedBox(height: 20),
                  const Text(
                    'Serious Side Effects:',
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.red),
                  ),
                  const SizedBox(height: 10),
                  ..._drugInfo!['serious_side_effects'].map<Widget>((effect) {
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 8),
                      child: Row(
                        children: [
                          const Icon(Icons.warning, color: Colors.red, size: 20),
                          const SizedBox(width: 10),
                          Expanded(child: Text(effect)),
                        ],
                      ),
                    );
                  }).toList(),
                ],
              )
            else if (!_isLoading)
              const Center(
                child: Text(
                  'Search for a drug to see information',
                  style: TextStyle(color: Colors.grey),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
