import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:typed_data';

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
  Uint8List? _imageBytes;
  final ImagePicker _picker = ImagePicker();

  void _msg(String m) => ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(m)));

  Future<void> _takePicture() async {
    try {
      final XFile? photo = await _picker.pickImage(source: ImageSource.camera);
      if (photo != null) {
        final bytes = await photo.readAsBytes();
        setState(() { _imageBytes = bytes; _analyzing = true; });
        await Future.delayed(const Duration(seconds: 3));
        if (mounted) setState(() { _analyzing = false; _done = true; });
      }
    } catch (e) { _msg('Camera: $e'); }
  }

  void _reset() => setState(() { _imageBytes = null; _analyzing = false; _done = false; });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(['Skincare AI', 'Scan', 'Tips', 'Profile'][_idx]), backgroundColor: Colors.purple.shade100),
      body: [_home(), _scan(), _tips(), _profile()][_idx],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _idx,
        onTap: (i) => setState(() => _idx = i),
        type: BottomNavigationBarType.fixed,
        selectedItemColor: Colors.purple,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.camera_alt), label: 'Scan'),
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
            child: const Row(children: [
              CircleAvatar(radius: 30, backgroundColor: Colors.white, child: Icon(Icons.face, size: 35, color: Colors.purple)),
              SizedBox(width: 16),
              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
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
          _card('Take Photo', Icons.camera_alt, Colors.teal, () { setState(() => _idx = 1); }),
          _card('Get Tips', Icons.lightbulb, Colors.orange, () => setState(() => _idx = 2)),
          _card('Hydration', Icons.water_drop, Colors.blue, () => _msg('Hydration: 72%')),
          _card('UV Check', Icons.wb_sunny, Colors.amber, () => _msg('UV Index: 6')),
        ]),
      ]),
    );
  }

  Widget _card(String t, IconData i, Color c, VoidCallback f) => Card(child: InkWell(onTap: f, child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [Icon(i, size: 36, color: c), const SizedBox(height: 8), Text(t, style: const TextStyle(fontWeight: FontWeight.w600))])));

  Widget _scan() {
    if (_analyzing) return const Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [CircularProgressIndicator(), SizedBox(height: 20), Text('Analyzing your skin...', style: TextStyle(fontSize: 18))]));
    if (_done && _imageBytes != null) return SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
      ClipRRect(borderRadius: BorderRadius.circular(16), child: Image.memory(_imageBytes!, width: 250, height: 250, fit: BoxFit.cover)),
      const SizedBox(height: 16),
      const Icon(Icons.check_circle, size: 50, color: Colors.green),
      const Text('Analysis Complete!', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
      const SizedBox(height: 16),
      _result('Hydration', 72), _result('Oiliness', 45), _result('Elasticity', 85), _result('Pores', 38),
      const SizedBox(height: 16),
      ElevatedButton(onPressed: _reset, child: const Text('Take New Photo')),
    ]));
    return Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      Icon(Icons.camera_alt, size: 80, color: Colors.purple.shade300),
      const SizedBox(height: 24),
      const Text('Skin Scanner', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
      const SizedBox(height: 8),
      Text('Take a photo for AI skin analysis', style: TextStyle(color: Colors.grey.shade600)),
      const SizedBox(height: 24),
      ElevatedButton.icon(onPressed: _takePicture, icon: const Icon(Icons.camera_alt), label: const Text('Open Camera'), style: ElevatedButton.styleFrom(backgroundColor: Colors.purple, foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16))),
    ]));
  }

  Widget _result(String label, int value) {
    Color c = value >= 70 ? Colors.green : value >= 50 ? Colors.orange : Colors.red;
    return Card(margin: const EdgeInsets.symmetric(vertical: 6), child: Padding(padding: const EdgeInsets.all(16), child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [Text(label), Container(padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4), decoration: BoxDecoration(color: c.withOpacity(0.2), borderRadius: BorderRadius.circular(12)), child: Text('$value%', style: TextStyle(color: c, fontWeight: FontWeight.bold)))])));
  }

  Widget _tips() {
    final tips = [{'t': 'Hydration is Key', 's': 'Drink 8 glasses of water daily', 'i': Icons.water_drop}, {'t': 'Sun Protection', 's': 'Apply SPF 30+ sunscreen', 'i': Icons.wb_sunny}, {'t': 'Gentle Cleansing', 's': 'Use a gentle cleanser twice daily', 'i': Icons.cleaning_services}, {'t': 'Sleep Well', 's': 'Get 7-9 hours of sleep', 'i': Icons.bedtime}];
    return ListView.builder(padding: const EdgeInsets.all(16), itemCount: tips.length, itemBuilder: (ctx, i) => Card(margin: const EdgeInsets.only(bottom: 12), child: ListTile(leading: CircleAvatar(backgroundColor: Colors.purple.shade100, child: Icon(tips[i]['i'] as IconData, color: Colors.purple)), title: Text(tips[i]['t'] as String, style: const TextStyle(fontWeight: FontWeight.bold)), subtitle: Text(tips[i]['s'] as String))));
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
      _opt(Icons.help, 'Help'),
      _opt(Icons.logout, 'Logout'),
    ]));
  }

  Widget _opt(IconData i, String t) => Card(margin: const EdgeInsets.only(bottom: 8), child: ListTile(leading: Icon(i, color: Colors.purple), title: Text(t), trailing: const Icon(Icons.chevron_right), onTap: () => _msg(t)));
}