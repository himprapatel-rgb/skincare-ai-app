import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Skincare AI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: Colors.purple), useMaterial3: true),
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
  int _idx = 0;
  bool _analyzing = false;
  bool _done = false;

  void _msg(String m) => ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(m)));

  void _analyze() {
    setState(() => _analyzing = true);
    Future.delayed(const Duration(seconds: 3), () {
      if (mounted) setState(() { _analyzing = false; _done = true; });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(['Skincare AI', 'Analysis', 'Tips', 'Profile'][_idx]), backgroundColor: Colors.purple.shade100),
      body: [_home(), _analysis(), _tips(), _profile()][_idx],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _idx,
        onTap: (i) => setState(() => _idx = i),
        type: BottomNavigationBarType.fixed,
        selectedItemColor: Colors.purple,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.camera_alt), label: 'Analysis'),
          BottomNavigationBarItem(icon: Icon(Icons.lightbulb), label: 'Tips'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }

  Widget _home() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(children: [
        Card(
          child: Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(borderRadius: BorderRadius.circular(12), gradient: LinearGradient(colors: [Colors.purple.shade300, Colors.purple.shade100])),
            child: Row(children: [
              const CircleAvatar(radius: 30, backgroundColor: Colors.white, child: Icon(Icons.face, size: 35, color: Colors.purple)),
              const SizedBox(width: 16),
              const Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('Welcome to Skincare AI', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
                Text('Your skin health assistant', style: TextStyle(color: Colors.white70)),
              ])),
            ]),
          ),
        ),
        const SizedBox(height: 20),
        const Text('Quick Actions', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        GridView.count(shrinkWrap: true, physics: const NeverScrollableScrollPhysics(), crossAxisCount: 2, mainAxisSpacing: 12, crossAxisSpacing: 12, childAspectRatio: 1.3, children: [
          _card('Scan Skin', Icons.camera_alt, Colors.teal, () { setState(() => _idx = 1); _analyze(); }),
          _card('Get Tips', Icons.lightbulb, Colors.orange, () => setState(() => _idx = 2)),
          _card('Hydration', Icons.water_drop, Colors.blue, () => _msg('Hydration: 72%')),
          _card('UV Check', Icons.wb_sunny, Colors.amber, () => _msg('UV Index: 6')),
        ]),
      ]),
    );
  }

  Widget _card(String t, IconData i, Color c, VoidCallback f) {
    return Card(child: InkWell(onTap: f, child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [Icon(i, size: 36, color: c), const SizedBox(height: 8), Text(t, style: const TextStyle(fontWeight: FontWeight.w600))])));
  }

  Widget _analysis() {
    if (_analyzing) return const Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [CircularProgressIndicator(), SizedBox(height: 20), Text('Analyzing...', style: TextStyle(fontSize: 18))]));
    if (_done) return SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
      const Icon(Icons.check_circle, size: 60, color: Colors.green),
      const SizedBox(height: 12),
      const Text('Analysis Complete!', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
      const SizedBox(height: 20),
      _result('Hydration', 72),
      _result('Oiliness', 45),
      _result('Elasticity', 85),
      _result('Pores', 38),
      const SizedBox(height: 20),
      ElevatedButton(onPressed: () => setState(() => _done = false), child: const Text('Analyze Again')),
    ]));
    return Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      Icon(Icons.camera_alt, size: 80, color: Colors.purple.shade300),
      const SizedBox(height: 24),
      const Text('Ready to Analyze', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
      const SizedBox(height: 24),
      ElevatedButton.icon(onPressed: _analyze, icon: const Icon(Icons.play_arrow), label: const Text('Start Analysis')),
    ]));
  }

  Widget _result(String label, int value) {
    Color c = value >= 70 ? Colors.green : value >= 50 ? Colors.orange : Colors.red;
    return Card(margin: const EdgeInsets.symmetric(vertical: 6), child: Padding(padding: const EdgeInsets.all(16), child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [Text(label, style: const TextStyle(fontWeight: FontWeight.w600)), Container(padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4), decoration: BoxDecoration(color: c.withOpacity(0.2), borderRadius: BorderRadius.circular(12)), child: Text('$value%', style: TextStyle(color: c, fontWeight: FontWeight.bold)))])));
  }

  Widget _tips() {
    final tips = [{'t': 'Hydration is Key', 's': 'Drink 8 glasses of water daily', 'i': Icons.water_drop}, {'t': 'Sun Protection', 's': 'Apply SPF 30+ sunscreen', 'i': Icons.wb_sunny}, {'t': 'Gentle Cleansing', 's': 'Use a gentle cleanser twice daily', 'i': Icons.cleaning_services}, {'t': 'Sleep Well', 's': 'Get 7-9 hours of sleep', 'i': Icons.bedtime}];
    return ListView.builder(padding: const EdgeInsets.all(16), itemCount: tips.length, itemBuilder: (ctx, i) => Card(margin: const EdgeInsets.only(bottom: 12), child: ListTile(leading: CircleAvatar(backgroundColor: Colors.purple.shade100, child: Icon(tips[i]['i'] as IconData, color: Colors.purple)), title: Text(tips[i]['t'] as String, style: const TextStyle(fontWeight: FontWeight.bold)), subtitle: Text(tips[i]['s'] as String), trailing: IconButton(icon: const Icon(Icons.bookmark_border), onPressed: () => _msg('Tip saved!')))));
  }

  Widget _profile() {
    return SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
      CircleAvatar(radius: 50, backgroundColor: Colors.purple.shade100, child: const Icon(Icons.person, size: 50, color: Colors.purple)),
      const SizedBox(height: 16),
      const Text('User', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
      const Text('user@example.com', style: TextStyle(color: Colors.grey)),
      const SizedBox(height: 24),
      _opt(Icons.settings, 'Settings'),
      _opt(Icons.notifications, 'Notifications'),
      _opt(Icons.help, 'Help & Support'),
      _opt(Icons.info, 'About'),
      _opt(Icons.logout, 'Logout'),
    ]));
  }

  Widget _opt(IconData i, String t) => Card(margin: const EdgeInsets.only(bottom: 8), child: ListTile(leading: Icon(i, color: Colors.purple), title: Text(t), trailing: const Icon(Icons.chevron_right), onTap: () => _msg(t)));
}