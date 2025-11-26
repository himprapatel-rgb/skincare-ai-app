import 'package:flutter/material.dart';

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

class _MainScreenState extends State<MainScreen> {
  int _currentIndex = 0;
  bool _isAnalyzing = false;
  bool _showResults = false;
  String _message = '';

  void _showMsg(String msg) {
    setState(() => _message = msg);
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) setState(() => _message = '');
    });
  }

  void _startAnalysis() {
    setState(() { _isAnalyzing = true; _showResults = false; });
    Future.delayed(const Duration(seconds: 3), () {
      if (mounted) setState(() { _isAnalyzing = false; _showResults = true; });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_getTitle()),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [IconButton(icon: const Icon(Icons.notifications), onPressed: () => _showMsg('No notifications'))],
      ),
      body: Stack(
        children: [
          _buildBody(),
          if (_message.isNotEmpty)
            Positioned(
              bottom: 100, left: 20, right: 20,
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(color: Colors.black87, borderRadius: BorderRadius.circular(8)),
                child: Text(_message, style: const TextStyle(color: Colors.white), textAlign: TextAlign.center),
              ),
            ),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (i) => setState(() => _currentIndex = i),
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.camera_alt), label: 'Analyze'),
          BottomNavigationBarItem(icon: Icon(Icons.history), label: 'History'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }

  String _getTitle() => ['Skincare AI', 'Skin Analysis', 'History', 'Profile'][_currentIndex];

  Widget _buildBody() {
    switch (_currentIndex) {
      case 0: return _buildHome();
      case 1: return _buildAnalysis();
      case 2: return _buildHistory();
      case 3: return _buildProfile();
      default: return _buildHome();
    }
  }

  Widget _buildHome() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(children: [
        Card(child: Padding(padding: const EdgeInsets.all(20), child: Column(children: [
          const Icon(Icons.face, size: 60, color: Colors.purple),
          const SizedBox(height: 12),
          const Text('Welcome!', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const Text('Your AI skincare assistant'),
        ]))),
        const SizedBox(height: 20),
        Row(children: [
          Expanded(child: _card(Icons.camera, 'Scan Skin', Colors.blue, () { setState(() => _currentIndex = 1); _startAnalysis(); })),
          const SizedBox(width: 12),
          Expanded(child: _card(Icons.lightbulb, 'Get Tips', Colors.orange, () => _showMsg('Tip: Apply sunscreen daily!'))),
        ]),
        const SizedBox(height: 12),
        Row(children: [
          Expanded(child: _card(Icons.water_drop, 'Hydration', Colors.cyan, () => _showMsg('Hydration Level: 72% - Good!'))),
          const SizedBox(width: 12),
          Expanded(child: _card(Icons.wb_sunny, 'UV Check', Colors.amber, () => _showMsg('UV Index: 5 - Moderate'))),
        ]),
        const SizedBox(height: 20),
        Card(child: Padding(padding: const EdgeInsets.all(16), child: Row(children: [
          const SizedBox(width: 50, height: 50, child: CircularProgressIndicator(value: 0.78, strokeWidth: 6)),
          const SizedBox(width: 20),
          Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Text('78/100', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            Text('Good skin health!', style: TextStyle(color: Colors.green[700])),
          ]),
        ]))),
      ]),
    );
  }

  Widget _card(IconData icon, String label, Color color, VoidCallback onTap) {
    return Card(child: InkWell(onTap: onTap, borderRadius: BorderRadius.circular(12),
      child: Padding(padding: const EdgeInsets.all(20), child: Column(children: [
        Icon(icon, size: 32, color: color),
        const SizedBox(height: 8),
        Text(label, style: const TextStyle(fontWeight: FontWeight.w500)),
      ]))));
  }

  Widget _buildAnalysis() {
    if (_isAnalyzing) {
      return const Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        CircularProgressIndicator(), SizedBox(height: 20),
        Text('Analyzing your skin...', style: TextStyle(fontSize: 18)),
        SizedBox(height: 8), Text('Please wait...'),
      ]));
    }
    if (_showResults) {
      return SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
        const Icon(Icons.check_circle, size: 60, color: Colors.green),
        const SizedBox(height: 16),
        const Text('Analysis Complete!', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
        const SizedBox(height: 20),
        _result('Hydration', '72%', Colors.blue),
        _result('Oiliness', '45%', Colors.orange),
        _result('Elasticity', '85%', Colors.green),
        _result('Pores', '38%', Colors.purple),
        _result('Wrinkles', '22%', Colors.red),
        _result('Dark Spots', '15%', Colors.brown),
        const SizedBox(height: 20),
        const Text('Recommendations:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        _tip('Drink 8 glasses of water daily'),
        _tip('Use SPF 30+ sunscreen'),
        _tip('Apply moisturizer twice daily'),
        const SizedBox(height: 20),
        ElevatedButton(onPressed: () => setState(() => _showResults = false), child: const Text('Analyze Again')),
      ]));
    }
    return Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      const Icon(Icons.camera_alt, size: 80, color: Colors.purple),
      const SizedBox(height: 20),
      const Text('Ready to Analyze', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
      const SizedBox(height: 8),
      const Text('Tap button to start skin analysis'),
      const SizedBox(height: 24),
      ElevatedButton.icon(onPressed: _startAnalysis, icon: const Icon(Icons.play_arrow), label: const Text('Start Analysis')),
    ]));
  }

  Widget _result(String label, String value, Color color) {
    return Card(child: Padding(padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
        Text(label, style: const TextStyle(fontSize: 16)),
        Container(padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
          decoration: BoxDecoration(color: color.withOpacity(0.2), borderRadius: BorderRadius.circular(12)),
          child: Text(value, style: TextStyle(color: color, fontWeight: FontWeight.bold))),
      ])));
  }

  Widget _tip(String text) {
    return Card(child: ListTile(leading: const Icon(Icons.check, color: Colors.green), title: Text(text)));
  }

  Widget _buildHistory() {
    return ListView.builder(padding: const EdgeInsets.all(16), itemCount: 5,
      itemBuilder: (context, i) => Card(margin: const EdgeInsets.only(bottom: 12),
        child: ListTile(
          leading: CircleAvatar(backgroundColor: Colors.purple[100], child: Text('${85 - i * 3}')),
          title: Text('Analysis ${5 - i}'),
          subtitle: Text('${i + 1} days ago - Score: ${85 - i * 3}/100'),
          trailing: const Icon(Icons.chevron_right),
          onTap: () => _showMsg('Viewing details for Analysis ${5 - i}'),
        )));
  }

  Widget _buildProfile() {
    return SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
      const CircleAvatar(radius: 50, backgroundColor: Colors.purple, child: Icon(Icons.person, size: 50, color: Colors.white)),
      const SizedBox(height: 16),
      const Text('User', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
      const Text('user@example.com'),
      const SizedBox(height: 24),
      _opt(Icons.edit, 'Edit Profile'),
      _opt(Icons.settings, 'Settings'),
      _opt(Icons.notifications, 'Notifications'),
      _opt(Icons.security, 'Privacy'),
      _opt(Icons.help, 'Help & Support'),
      _opt(Icons.info, 'About'),
      _opt(Icons.logout, 'Logout'),
    ]));
  }

  Widget _opt(IconData icon, String label) {
    return Card(margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(leading: Icon(icon), title: Text(label), trailing: const Icon(Icons.chevron_right),
        onTap: () => _showMsg('$label clicked!')));
  }
}