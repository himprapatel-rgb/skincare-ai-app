import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:math';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Skincare AI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.purple),
        useMaterial3: true,
      ),
      home: const MainScreen(),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> with TickerProviderStateMixin {
  int _currentIndex = 0;
  bool _isAnalyzing = false;
  bool _showResults = false;
  bool _cameraActive = false;
  Map<String, int> _results = {};
  List<Map<String, dynamic>> _skincareTips = [];
  late AnimationController _pulseController;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    )..repeat(reverse: true);
    _loadTips();
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  void _loadTips() {
    _skincareTips = [
      {'title': 'Hydration is Key', 'tip': 'Drink 8 glasses of water daily for healthy skin', 'icon': Icons.water_drop},
      {'title': 'Sun Protection', 'tip': 'Apply SPF 30+ sunscreen every morning', 'icon': Icons.wb_sunny},
      {'title': 'Gentle Cleansing', 'tip': 'Use a gentle cleanser twice daily', 'icon': Icons.cleaning_services},
      {'title': 'Sleep Well', 'tip': 'Get 7-9 hours of sleep for skin repair', 'icon': Icons.bedtime},
      {'title': 'Vitamin C', 'tip': 'Use Vitamin C serum for brighter skin', 'icon': Icons.brightness_high},
      {'title': 'Moisturize', 'tip': 'Apply moisturizer on damp skin', 'icon': Icons.opacity},
    ];
  }

  void _showMsg(String msg) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(msg), duration: const Duration(seconds: 2)),
    );
  }

  void _startCamera() {
    setState(() {
      _cameraActive = true;
      _showResults = false;
    });
  }

  void _captureAndAnalyze() {
    setState(() {
      _cameraActive = false;
      _isAnalyzing = true;
    });
    
    Future.delayed(const Duration(seconds: 3), () {
      if (mounted) {
        setState(() {
          _isAnalyzing = false;
          _showResults = true;
          final random = Random();
          _results = {
            'Hydration': 65 + random.nextInt(25),
            'Oiliness': 30 + random.nextInt(40),
            'Elasticity': 70 + random.nextInt(25),
            'Pores': 25 + random.nextInt(35),
            'Wrinkles': 10 + random.nextInt(30),
            'Dark Spots': 15 + random.nextInt(25),
            'Redness': 10 + random.nextInt(30),
            'Texture': 60 + random.nextInt(35),
          };
        });
      }
    });
  }

  void _resetAnalysis() {
    setState(() {
      _cameraActive = false;
      _isAnalyzing = false;
      _showResults = false;
      _results = {};
    });
  }

  String _getRecommendation(String metric, int value) {
    if (metric == 'Hydration') {
      if (value < 50) return 'Increase water intake and use hydrating serums';
      if (value < 75) return 'Good hydration! Maintain your routine';
      return 'Excellent hydration levels!';
    } else if (metric == 'Oiliness') {
      if (value > 60) return 'Use oil-free products and clay masks';
      if (value > 40) return 'Balanced oil production';
      return 'Low oiliness - add lightweight moisturizer';
    } else if (metric == 'Elasticity') {
      if (value < 60) return 'Use retinol and collagen-boosting products';
      if (value < 80) return 'Good elasticity - keep moisturizing';
      return 'Excellent skin elasticity!';
    }
    return 'Keep up your skincare routine!';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(['Skincare AI', 'Skin Analysis', 'Tips', 'History', 'Profile'][_currentIndex]),
        backgroundColor: Colors.purple.shade100,
        foregroundColor: Colors.purple.shade900,
        actions: [
          IconButton(icon: const Icon(Icons.notifications_outlined), onPressed: () => _showMsg('No new notifications')),
        ],
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.purple.shade50, Colors.white],
          ),
        ),
        child: [_buildHome(), _buildAnalysis(), _buildTips(), _buildHistory(), _buildProfile()][_currentIndex],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (i) => setState(() => _currentIndex = i),
        type: BottomNavigationBarType.fixed,
        selectedItemColor: Colors.purple,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.camera_alt), label: 'Analyze'),
          BottomNavigationBarItem(icon: Icon(Icons.lightbulb), label: 'Tips'),
          BottomNavigationBarItem(icon: Icon(Icons.history), label: 'History'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }

  Widget _buildHome() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Card(
            elevation: 4,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(16),
                gradient: LinearGradient(colors: [Colors.purple.shade300, Colors.purple.shade100]),
              ),
              child: Row(
                children: [
                  CircleAvatar(radius: 30, backgroundColor: Colors.white, child: Icon(Icons.face, size: 35, color: Colors.purple)),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Welcome to Skincare AI', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
                        const SizedBox(height: 4),
                        Text('Your personal skin health assistant', style: TextStyle(color: Colors.white.withOpacity(0.9))),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          const Text('Quick Actions', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          GridView.count(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            crossAxisCount: 2,
            mainAxisSpacing: 12,
            crossAxisSpacing: 12,
            childAspectRatio: 1.3,
            children: [
              _buildActionCard('Scan Skin', Icons.camera_alt, Colors.teal, () { setState(() => _currentIndex = 1); _startCamera(); }),
              _buildActionCard('Get Tips', Icons.lightbulb, Colors.orange, () => setState(() => _currentIndex = 2)),
              _buildActionCard('Hydration', Icons.water_drop, Colors.blue, () => _showMsg('Hydration Level: 72% - Good!')),
              _buildActionCard('UV Index', Icons.wb_sunny, Colors.amber, () => _showMsg('UV Index: 6 - Use SPF 30+')),
            ],
          ),
          const SizedBox(height: 24),
          const Text('Your Skin Score', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                children: [
                  SizedBox(
                    width: 80,
                    height: 80,
                    child: Stack(
                      children: [
                        CircularProgressIndicator(value: 0.78, strokeWidth: 8, backgroundColor: Colors.grey.shade200, color: Colors.purple),
                        const Center(child: Text('78', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold))),
                      ],
                    ),
                  ),
                  const SizedBox(width: 20),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Good Skin Health!', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.green)),
                        const SizedBox(height: 4),
                        Text('Based on your last analysis', style: TextStyle(color: Colors.grey.shade600)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionCard(String title, IconData icon, Color color, VoidCallback onTap) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 36, color: color),
              const SizedBox(height: 8),
              Text(title, style: const TextStyle(fontWeight: FontWeight.w600)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAnalysis() {
    if (_cameraActive) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            AnimatedBuilder(
              animation: _pulseController,
              builder: (context, child) {
                return Container(
                  width: 250 + (_pulseController.value * 20),
                  height: 250 + (_pulseController.value * 20),
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.purple.withOpacity(0.5), width: 3),
                    color: Colors.purple.shade50,
                  ),
                  child: Icon(Icons.face, size: 120, color: Colors.purple.shade300),
                );
              },
            ),
            const SizedBox(height: 24),
            const Text('Position your face in the circle', style: TextStyle(fontSize: 18)),
            const SizedBox(height: 8),
            Text('Ensure good lighting', style: TextStyle(color: Colors.grey.shade600)),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: _captureAndAnalyze,
              icon: const Icon(Icons.camera),
              label: const Text('Capture & Analyze'),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.purple, foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16)),
            ),
            TextButton(onPressed: _resetAnalysis, child: const Text('Cancel')),
          ],
        ),
      );
    }
    if (_isAnalyzing) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const SizedBox(width: 80, height: 80, child: CircularProgressIndicator(strokeWidth: 6)),
            const SizedBox(height: 24),
            const Text('Analyzing your skin...', style: TextStyle(fontSize: 18)),
            const SizedBox(height: 8),
            Text('AI is processing your image', style: TextStyle(color: Colors.grey.shade600)),
          ],
        ),
      );
    }
    if (_showResults) {
      return SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Icon(Icons.check_circle, size: 60, color: Colors.green),
            const SizedBox(height: 12),
            const Text('Analysis Complete!', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 20),
            ..._results.entries.map((e) => _buildResultItem(e.key, e.value)),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: () { _resetAnalysis(); _startCamera(); },
              icon: const Icon(Icons.refresh),
              label: const Text('Analyze Again'),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.purple, foregroundColor: Colors.white),
            ),
          ],
        ),
      );
    }
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.camera_alt, size: 80, color: Colors.purple.shade300),
          const SizedBox(height: 24),
          const Text('Ready to Analyze', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Text('Tap below to start skin analysis', style: TextStyle(color: Colors.grey.shade600)),
          const SizedBox(height: 24),
          ElevatedButton.icon(
            onPressed: _startCamera,
            icon: const Icon(Icons.play_arrow),
            label: const Text('Start Analysis'),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.purple, foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16)),
          ),
        ],
      ),
    );
  }

  Widget _buildResultItem(String label, int value) {
    Color color = value >= 70 ? Colors.green : value >= 50 ? Colors.orange : Colors.red;
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(label, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16)),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                  decoration: BoxDecoration(color: color.withOpacity(0.2), borderRadius: BorderRadius.circular(12)),
                  child: Text('$value%', style: TextStyle(color: color, fontWeight: FontWeight.bold)),
                ),
              ],
            ),
            const SizedBox(height: 8),
            LinearProgressIndicator(value: value / 100, backgroundColor: Colors.grey.shade200, color: color),
            const SizedBox(height: 8),
            Text(_getRecommendation(label, value), style: TextStyle(color: Colors.grey.shade600, fontSize: 13)),
          ],
        ),
      ),
    );
  }

  Widget _buildTips() {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _skincareTips.length,
      itemBuilder: (context, index) {
        final tip = _skincareTips[index];
        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: Colors.purple.shade100,
              child: Icon(tip['icon'], color: Colors.purple),
            ),
            title: Text(tip['title'], style: const TextStyle(fontWeight: FontWeight.bold)),
            subtitle: Text(tip['tip']),
            trailing: IconButton(
              icon: const Icon(Icons.bookmark_border),
              onPressed: () => _showMsg('Tip saved!'),
            ),
          ),
        );
      },
    );
  }

  Widget _buildHistory() {
    final history = List.generate(7, (i) => {
      'date': DateTime.now().subtract(Duration(days: i)),
      'score': 75 + (i % 3) * 5 - i,
    });
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: history.length,
      itemBuilder: (context, index) {
        final item = history[index];
        final date = item['date'] as DateTime;
        final score = item['score'] as int;
        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: score >= 75 ? Colors.green.shade100 : Colors.orange.shade100,
              child: Text('$score', style: TextStyle(fontWeight: FontWeight.bold, color: score >= 75 ? Colors.green : Colors.orange)),
            ),
            title: Text('Analysis ${history.length - index}'),
            subtitle: Text('${date.day}/${date.month}/${date.year}'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => _showMsg('Viewing analysis from ${date.day}/${date.month}'),
          ),
        );
      },
    );
  }

  Widget _buildProfile() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          CircleAvatar(radius: 50, backgroundColor: Colors.purple.shade100, child: const Icon(Icons.person, size: 50, color: Colors.purple)),
          const SizedBox(height: 16),
          const Text('User', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          Text('user@example.com', style: TextStyle(color: Colors.grey.shade600)),
          const SizedBox(height: 24),
          _buildProfileOption(Icons.settings, 'Settings', () => _showMsg('Settings')),
          _buildProfileOption(Icons.notifications, 'Notifications', () => _showMsg('Notifications')),
          _buildProfileOption(Icons.help, 'Help & Support', () => _showMsg('Help')),
          _buildProfileOption(Icons.info, 'About', () => _showMsg('Skincare AI v1.0')),
          _buildProfileOption(Icons.logout, 'Logout', () => _showMsg('Logout')),
        ],
      ),
    );
  }

  Widget _buildProfileOption(IconData icon, String title, VoidCallback onTap) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Icon(icon, color: Colors.purple),
        title: Text(title),
        trailing: const Icon(Icons.chevron_right),
        onTap: onTap,
      ),
    );
  }
}
}