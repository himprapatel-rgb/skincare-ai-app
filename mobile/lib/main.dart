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
  Uint8List? _img;
  final _picker = ImagePicker();

  void _msg(String m) => ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(m)));

  Future<void> _openCamera() async {
    final XFile? photo = await _picker.pickImage(source: ImageSource.camera);
    if (photo != null) {
      final bytes = await photo.readAsBytes();
      setState(() { _img = bytes; _analyzing = true; });
      await Future.delayed(const Duration(seconds: 3));
      if (mounted) setState(() { _analyzing = false; _done = true; });
    }
  }

  void _reset() => setState(() { _img = null; _analyzing = false; _done = false; });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(['Skincare AI', 'Camera', 'Tips', 'Profile'][_idx]), backgroundColor: Colors.purple.shade100),
      body: [_home(), _camera(), _tips(), _profile()][_idx],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _idx,
        onTap: (i) => setState(() => _idx = i),
        type: BottomNavigationBarType.fixed,
        selectedItemColor: Colors.purple,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.camera_alt), label: 'Camera'),
          BottomNavigationBarItem(icon: Icon(Icons.lightbulb), label: 'Tips'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }

  Widget _home() {
    return SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
      Card(child: Container(padding: const EdgeInsets.all(20), decoration: BoxDecoration(borderRadius: BorderRadius.circular(12), gradient: LinearGradient(colors: [Colors.purple.shade300, Colors.purple.shade100])),
        child: const Row(children: [CircleAvatar(radius: 30, backgroundColor: Colors.white, child: Icon(Icons.face, size: 35, color: Colors.purple)), SizedBox(width: 16),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text('Skincare AI', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)), Text('Take photo to analyze skin', style: TextStyle(color: Colors.white70))]))]))),
      const SizedBox(height: 20),
      GridView.count(shrinkWrap: true, physics: const NeverScrollableScrollPhysics(), crossAxisCount: 2, mainAxisSpacing: 12, crossAxisSpacing: 12, childAspectRatio: 1.3, children: [
        _card('Take Photo', Icons.camera_alt, Colors.teal, () { setState(() => _idx = 1); _openCamera(); }),
        _card('Tips', Icons.lightbulb, Colors.orange, () => setState(() => _idx = 2)),
      ]),
    ]));
  }

  Widget _card(String t, IconData i, Color c, VoidCallback f) => Card(child: InkWell(onTap: f, child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [Icon(i, size: 36, color: c), const SizedBox(height: 8), Text(t)])));

  Widget _camera() {
    if (_analyzing) return const Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [CircularProgressIndicator(), SizedBox(height: 20), Text('Analyzing...', style: TextStyle(fontSize: 18))]));
    if (_done && _img != null) return SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
      ClipRRect(borderRadius: BorderRadius.circular(16), child: Image.memory(_img!, width: 200, height: 200, fit: BoxFit.cover)),
      const SizedBox(height: 16),
      const Icon(Icons.check_circle, size: 50, color: Colors.green),
      const Text('Analysis Complete!', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
      const SizedBox(height: 16),
      _res('Hydration', 72), _res('Oiliness', 45), _res('Elasticity', 85),
      const SizedBox(height: 16),
      ElevatedButton(onPressed: _reset, child: const Text('Take New Photo')),
    ]));
    return Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      Icon(Icons.camera_alt, size: 80, color: Colors.purple.shade300),
      const SizedBox(height: 24),
      const Text('Skin Scanner', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
      const Text('Take a photo for AI skin analysis'),
      const SizedBox(height: 24),
      ElevatedButton.icon(onPressed: _openCamera, icon: const Icon(Icons.camera_alt), label: const Text('Open Camera'), style: ElevatedButton.styleFrom(backgroundColor: Colors.purple, foregroundColor: Colors.white)),
    ]));
  }

  Widget _res(String l, int v) => Card(margin: const EdgeInsets.symmetric(vertical: 4), child: Padding(padding: const EdgeInsets.all(12), child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [Text(l), Text('$v%', style: TextStyle(color: v >= 70 ? Colors.green : Colors.orange, fontWeight: FontWeight.bold))])));

  Widget _tips() => ListView(padding: const EdgeInsets.all(16), children: [
    _tip('Hydration', 'Drink 8 glasses of water', Icons.water_drop),
    _tip('Sun Protection', 'Apply SPF 30+ daily', Icons.wb_sunny),
    _tip('Cleanse', 'Wash face twice daily', Icons.cleaning_services),
  ]);

  Widget _tip(String t, String s, IconData i) => Card(margin: const EdgeInsets.only(bottom: 12), child: ListTile(leading: CircleAvatar(backgroundColor: Colors.purple.shade100, child: Icon(i, color: Colors.purple)), title: Text(t, style: const TextStyle(fontWeight: FontWeight.bold)), subtitle: Text(s)));

  Widget _profile() => SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
    CircleAvatar(radius: 50, backgroundColor: Colors.purple.shade100, child: const Icon(Icons.person, size: 50, color: Colors.purple)),
    const SizedBox(height: 16),
    const Text('User', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
    const SizedBox(height: 24),
    _opt(Icons.settings, 'Settings'),
    _opt(Icons.help, 'Help'),
    _opt(Icons.logout, 'Logout'),
  ]));

  Widget _opt(IconData i, String t) => Card(margin: const EdgeInsets.only(bottom: 8), child: ListTile(leading: Icon(i, color: Colors.purple), title: Text(t), onTap: () => _msg(t)));
}
}