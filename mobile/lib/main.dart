import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:typed_data';
import 'dart:math';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Skincare AI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.deepPurple,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      home: const MainScreen(),
    );
  }
}

// AI Recommendation Engine
class SkincareAI {
  static Map<String, dynamic> getPersonalizedRoutine(Map<String, int> metrics) {
    List<String> morning = [];
    List<String> evening = [];
    List<String> products = [];
    
    if (metrics['hydration']! < 60) {
      morning.add('Apply hyaluronic acid serum');
      evening.add('Use overnight hydrating mask');
      products.add('Hydrating Serum - \$24.99');
    }
    if (metrics['oiliness']! > 50) {
      morning.add('Use oil-free moisturizer');
      evening.add('Apply niacinamide serum');
      products.add('Oil Control Gel - \$19.99');
    }
    if (metrics['elasticity']! < 70) {
      morning.add('Apply vitamin C serum');
      evening.add('Use retinol treatment');
      products.add('Retinol Cream - \$34.99');
    }
    if (metrics['pores']! > 40) {
      morning.add('Use pore-minimizing primer');
      evening.add('Apply BHA exfoliant');
      products.add('Pore Refining Serum - \$29.99');
    }
    
    morning.add('Apply SPF 50 sunscreen');
    evening.add('Double cleanse before bed');
    
    return {'morning': morning, 'evening': evening, 'products': products};
  }
  
  static String getSkinScore(Map<String, int> metrics) {
    double score = (metrics['hydration']! + metrics['elasticity']! + 
                   (100 - metrics['oiliness']!) + (100 - metrics['pores']!)) / 4;
    return score.toStringAsFixed(0);
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});
  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> with TickerProviderStateMixin {
  int _selectedIndex = 0;
  Uint8List? _imageBytes;
  bool _isAnalyzing = false;
  bool _showResults = false;
  late AnimationController _pulseController;
  
  Map<String, int> _analysisResults = {
    'hydration': 0, 'oiliness': 0, 'elasticity': 0, 'pores': 0
  };
  
  List<Map<String, dynamic>> _analysisHistory = [];
  
  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..repeat(reverse: true);
  }
  
  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  Future<void> _pickImage() async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);
    if (pickedFile != null) {
      final bytes = await pickedFile.readAsBytes();
      setState(() {
        _imageBytes = bytes;
        _isAnalyzing = true;
      });
      await Future.delayed(const Duration(seconds: 3));
      final random = Random();
      setState(() {
        _analysisResults = {
          'hydration': 50 + random.nextInt(40),
          'oiliness': 20 + random.nextInt(50),
          'elasticity': 60 + random.nextInt(35),
          'pores': 20 + random.nextInt(40),
        };
        _isAnalyzing = false;
        _showResults = true;
        _analysisHistory.insert(0, {
          'date': DateTime.now().toString().substring(0, 16),
          'results': Map<String, int>.from(_analysisResults),
          'score': SkincareAI.getSkinScore(_analysisResults)
        });
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: AnimatedSwitcher(
        duration: const Duration(milliseconds: 300),
        child: _buildCurrentScreen(),
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) => setState(() => _selectedIndex = index),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.camera_alt), label: 'Scan'),
          NavigationDestination(icon: Icon(Icons.shopping_bag), label: 'Products'),
          NavigationDestination(icon: Icon(Icons.history), label: 'History'),
          NavigationDestination(icon: Icon(Icons.tips_and_updates), label: 'Tips'),
          NavigationDestination(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }

  Widget _buildCurrentScreen() {
    switch (_selectedIndex) {
      case 0: return _buildHomeScreen();
      case 1: return _buildCameraScreen();
      case 2: return _buildProductsScreen();
      case 3: return _buildHistoryScreen();
      case 4: return _buildTipsScreen();
      case 5: return _buildProfileScreen();
      default: return _buildHomeScreen();
    }
  }

  Widget _buildHomeScreen() {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Colors.deepPurple.shade100, Colors.white],
        ),
      ),
      child: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Welcome Back!', style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Text('Your skin health journey', style: Theme.of(context).textTheme.bodyLarge?.copyWith(color: Colors.grey)),
              const SizedBox(height: 24),
              if (_showResults) ...[
                _buildSkinScoreCard(),
                const SizedBox(height: 16),
                _buildQuickStats(),
                const SizedBox(height: 16),
                _buildRoutineCard(),
              ] else
                _buildStartAnalysisCard(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSkinScoreCard() {
    final score = SkincareAI.getSkinScore(_analysisResults);
    return Card(
      elevation: 4,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          gradient: LinearGradient(colors: [Colors.deepPurple, Colors.deepPurple.shade300]),
        ),
        child: Row(
          children: [
            AnimatedBuilder(
              animation: _pulseController,
              builder: (context, child) => Transform.scale(
                scale: 1.0 + (_pulseController.value * 0.1),
                child: Container(
                  width: 80, height: 80,
                  decoration: BoxDecoration(shape: BoxShape.circle, color: Colors.white.withOpacity(0.2)),
                  child: Center(child: Text(score, style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white))),
                ),
              ),
            ),
            const SizedBox(width: 20),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Skin Score', style: TextStyle(color: Colors.white70, fontSize: 14)),
                  Text(int.parse(score) >= 70 ? 'Excellent!' : int.parse(score) >= 50 ? 'Good' : 'Needs Care',
                    style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickStats() {
    return Row(
      children: [
        Expanded(child: _buildStatCard('Hydration', _analysisResults['hydration']!, Colors.blue)),
        const SizedBox(width: 8),
        Expanded(child: _buildStatCard('Elasticity', _analysisResults['elasticity']!, Colors.green)),
      ],
    );
  }

  Widget _buildStatCard(String label, int value, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text(label, style: TextStyle(color: Colors.grey.shade600, fontSize: 12)),
            const SizedBox(height: 8),
            Stack(
              alignment: Alignment.center,
              children: [
                SizedBox(
                  width: 60, height: 60,
                  child: CircularProgressIndicator(value: value / 100, strokeWidth: 6, backgroundColor: Colors.grey.shade200, color: color),
                ),
                Text('$value%', style: TextStyle(fontWeight: FontWeight.bold, color: color)),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRoutineCard() {
    final routine = SkincareAI.getPersonalizedRoutine(_analysisResults);
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.wb_sunny, color: Colors.orange.shade400),
                const SizedBox(width: 8),
                const Text('Your Personalized Routine', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              ],
            ),
            const SizedBox(height: 12),
            const Text('Morning', style: TextStyle(fontWeight: FontWeight.w600, color: Colors.deepPurple)),
            ...List<Widget>.from((routine['morning'] as List).map((step) => Padding(
              padding: const EdgeInsets.only(left: 16, top: 4),
              child: Text('• $step', style: const TextStyle(fontSize: 13)),
            ))),
            const SizedBox(height: 8),
            const Text('Evening', style: TextStyle(fontWeight: FontWeight.w600, color: Colors.deepPurple)),
            ...List<Widget>.from((routine['evening'] as List).map((step) => Padding(
              padding: const EdgeInsets.only(left: 16, top: 4),
              child: Text('• $step', style: const TextStyle(fontSize: 13)),
            ))),
          ],
        ),
      ),
    );
  }

  Widget _buildStartAnalysisCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            Icon(Icons.face_retouching_natural, size: 80, color: Colors.deepPurple.shade200),
            const SizedBox(height: 16),
            const Text('Start Your Skin Analysis', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text('Get personalized skincare recommendations', style: TextStyle(color: Colors.grey.shade600)),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: () => setState(() => _selectedIndex = 1),
              icon: const Icon(Icons.camera_alt),
              label: const Text('Scan Now'),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.deepPurple, foregroundColor: Colors.white),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCameraScreen() {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Colors.deepPurple.shade50, Colors.white],
        ),
      ),
      child: SafeArea(
        child: _isAnalyzing
            ? _buildAnalyzingView()
            : _showResults
                ? _buildResultsView()
                : _buildCameraPrompt(),
      ),
    );
  }

  Widget _buildCameraPrompt() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 200, height: 200,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(color: Colors.deepPurple, width: 3),
              color: Colors.deepPurple.shade50,
            ),
            child: Icon(Icons.face, size: 100, color: Colors.deepPurple.shade300),
          ),
          const SizedBox(height: 32),
          const Text('Face Scanner', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Text('Position your face in the circle', style: TextStyle(color: Colors.grey.shade600)),
          const SizedBox(height: 32),
          ElevatedButton.icon(
            onPressed: _pickImage,
            icon: const Icon(Icons.camera_alt),
            label: const Text('Start Scan'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.deepPurple,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAnalyzingView() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          AnimatedBuilder(
            animation: _pulseController,
            builder: (context, child) => Transform.scale(
              scale: 1.0 + (_pulseController.value * 0.2),
              child: Container(
                width: 150, height: 150,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: RadialGradient(colors: [Colors.deepPurple.shade200, Colors.deepPurple]),
                ),
                child: const Icon(Icons.face_retouching_natural, size: 80, color: Colors.white),
              ),
            ),
          ),
          const SizedBox(height: 32),
          const Text('Analyzing Your Skin...', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          const CircularProgressIndicator(),
        ],
      ),
    );
  }

  Widget _buildResultsView() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        children: [
          const Text('Analysis Complete', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          _buildMetricBar('Hydration', _analysisResults['hydration']!, Colors.blue),
          _buildMetricBar('Oiliness', _analysisResults['oiliness']!, Colors.orange),
          _buildMetricBar('Elasticity', _analysisResults['elasticity']!, Colors.green),
          _buildMetricBar('Pores', _analysisResults['pores']!, Colors.red),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: () => setState(() { _showResults = false; _selectedIndex = 0; }),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.deepPurple, foregroundColor: Colors.white),
            child: const Text('View Recommendations'),
          ),
        ],
      ),
    );
  }

  Widget _buildMetricBar(String label, int value, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(label, style: const TextStyle(fontWeight: FontWeight.w500)),
              Text('$value%', style: TextStyle(fontWeight: FontWeight.bold, color: color)),
            ],
          ),
          const SizedBox(height: 8),
          ClipRRect(
            borderRadius: BorderRadius.circular(10),
            child: LinearProgressIndicator(value: value / 100, minHeight: 12, backgroundColor: Colors.grey.shade200, color: color),
          ),
        ],
      ),
    );
  }

  Widget _buildProductsScreen() {
    final routine = SkincareAI.getPersonalizedRoutine(_analysisResults);
    final products = routine['products'] as List;
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Colors.deepPurple.shade50, Colors.white],
        ),
      ),
      child: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                children: [
                  Icon(Icons.shopping_bag, color: Colors.deepPurple, size: 28),
                  const SizedBox(width: 12),
                  const Text('Recommended Products', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            Expanded(
              child: products.isEmpty
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.face_retouching_natural, size: 80, color: Colors.grey.shade300),
                          const SizedBox(height: 16),
                          Text('Complete a skin scan first', style: TextStyle(color: Colors.grey.shade600, fontSize: 16)),
                          const SizedBox(height: 8),
                          ElevatedButton(
                            onPressed: () => setState(() => _selectedIndex = 1),
                            child: const Text('Start Scan'),
                          ),
                        ],
                      ),
                    )
                  : ListView.builder(
                      padding: const EdgeInsets.symmetric(horizontal: 20),
                      itemCount: products.length,
                      itemBuilder: (context, index) => Card(
                        margin: const EdgeInsets.only(bottom: 12),
                        child: ListTile(
                          leading: Container(
                            width: 50, height: 50,
                            decoration: BoxDecoration(
                              color: Colors.deepPurple.shade100,
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: const Icon(Icons.spa, color: Colors.deepPurple),
                          ),
                          title: Text(products[index].toString().split(' - ')[0]),
                          subtitle: Text(products[index].toString().split(' - ')[1], style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.green)),
                          trailing: ElevatedButton(
                            onPressed: () {},
                            style: ElevatedButton.styleFrom(backgroundColor: Colors.deepPurple, foregroundColor: Colors.white),
                            child: const Text('Buy'),
                          ),
                        ),
                      ),
                    ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHistoryScreen() {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Colors.deepPurple.shade50, Colors.white],
        ),
      ),
      child: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                children: [
                  Icon(Icons.history, color: Colors.deepPurple, size: 28),
                  const SizedBox(width: 12),
                  const Text('Analysis History', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            Expanded(
              child: _analysisHistory.isEmpty
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.history, size: 80, color: Colors.grey.shade300),
                          const SizedBox(height: 16),
                          Text('No analysis history yet', style: TextStyle(color: Colors.grey.shade600, fontSize: 16)),
                        ],
                      ),
                    )
                  : ListView.builder(
                      padding: const EdgeInsets.symmetric(horizontal: 20),
                      itemCount: _analysisHistory.length,
                      itemBuilder: (context, index) {
                        final item = _analysisHistory[index];
                        return Card(
                          margin: const EdgeInsets.only(bottom: 12),
                          child: ExpansionTile(
                            leading: Container(
                              width: 50, height: 50,
                              decoration: BoxDecoration(
                                color: Colors.deepPurple,
                                borderRadius: BorderRadius.circular(25),
                              ),
                              child: Center(
                                child: Text(item['score'], style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18)),
                              ),
                            ),
                            title: Text('Skin Score: ${item['score']}', style: const TextStyle(fontWeight: FontWeight.bold)),
                            subtitle: Text(item['date']),
                            children: [
                              Padding(
                                padding: const EdgeInsets.all(16),
                                child: Column(
                                  children: [
                                    _buildMiniMetric('Hydration', (item['results'] as Map)['hydration']),
                                    _buildMiniMetric('Oiliness', (item['results'] as Map)['oiliness']),
                                    _buildMiniMetric('Elasticity', (item['results'] as Map)['elasticity']),
                                    _buildMiniMetric('Pores', (item['results'] as Map)['pores']),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMiniMetric(String label, int value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [Text(label), Text('$value%', style: const TextStyle(fontWeight: FontWeight.bold))],
      ),
    );
  }

  Widget _buildTipsScreen() {
    final tips = [
      {'icon': Icons.water_drop, 'title': 'Stay Hydrated', 'desc': 'Drink 8 glasses of water daily for glowing skin'},
      {'icon': Icons.wb_sunny, 'title': 'Sun Protection', 'desc': 'Always wear SPF 30+ sunscreen'},
      {'icon': Icons.nightlight, 'title': 'Beauty Sleep', 'desc': 'Get 7-8 hours of quality sleep'},
      {'icon': Icons.restaurant, 'title': 'Healthy Diet', 'desc': 'Eat antioxidant-rich foods'},
      {'icon': Icons.self_improvement, 'title': 'Stress Less', 'desc': 'Practice meditation daily'},
      {'icon': Icons.cleaning_services, 'title': 'Cleanse Properly', 'desc': 'Double cleanse at night'},
    ];
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Colors.deepPurple.shade50, Colors.white],
        ),
      ),
      child: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                children: [
                  Icon(Icons.tips_and_updates, color: Colors.deepPurple, size: 28),
                  const SizedBox(width: 12),
                  const Text('Skincare Tips', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                itemCount: tips.length,
                itemBuilder: (context, index) => Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    leading: Container(
                      width: 50, height: 50,
                      decoration: BoxDecoration(
                        gradient: LinearGradient(colors: [Colors.deepPurple.shade300, Colors.deepPurple]),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Icon(tips[index]['icon'] as IconData, color: Colors.white),
                    ),
                    title: Text(tips[index]['title'] as String, style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text(tips[index]['desc'] as String),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProfileScreen() {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Colors.deepPurple.shade50, Colors.white],
        ),
      ),
      child: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              const SizedBox(height: 20),
              Container(
                width: 120, height: 120,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: LinearGradient(colors: [Colors.deepPurple.shade300, Colors.deepPurple]),
                ),
                child: const Icon(Icons.person, size: 60, color: Colors.white),
              ),
              const SizedBox(height: 16),
              const Text('User Profile', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Text('Track your skincare journey', style: TextStyle(color: Colors.grey.shade600)),
              const SizedBox(height: 32),
              _buildProfileStat('Total Scans', '${_analysisHistory.length}'),
              _buildProfileStat('Best Score', _analysisHistory.isEmpty ? '-' : _analysisHistory.map((e) => int.parse(e['score'])).reduce((a, b) => a > b ? a : b).toString()),
              _buildProfileStat('Member Since', 'Today'),
              const SizedBox(height: 24),
              Card(
                child: ListTile(
                  leading: const Icon(Icons.settings, color: Colors.deepPurple),
                  title: const Text('Settings'),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {},
                ),
              ),
              Card(
                child: ListTile(
                  leading: const Icon(Icons.help, color: Colors.deepPurple),
                  title: const Text('Help & Support'),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {},
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildProfileStat(String label, String value) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: const TextStyle(fontSize: 16)),
            Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.deepPurple)),
          ],
        ),
      ),
    );
  }
}