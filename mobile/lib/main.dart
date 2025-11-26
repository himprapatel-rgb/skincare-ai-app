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
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _selectedIndex = 0;

  final List<Widget> _pages = [
    const HomeContent(),
    const AnalysisPage(),
    const HistoryPage(),
    const ProfilePage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.camera_alt), label: 'Analyze'),
          NavigationDestination(icon: Icon(Icons.history), label: 'History'),
          NavigationDestination(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}

class HomeContent extends StatelessWidget {
  const HomeContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Skincare AI'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    Icon(Icons.face, size: 60, color: Theme.of(context).colorScheme.primary),
                    const SizedBox(height: 12),
                    const Text('Welcome to Skincare AI', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    const Text('Your AI-powered skincare assistant', textAlign: TextAlign.center),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),
            const Text('Quick Actions', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(child: _buildActionCard(context, Icons.camera_alt, 'Scan Skin', Colors.blue)),
                const SizedBox(width: 12),
                Expanded(child: _buildActionCard(context, Icons.tips_and_updates, 'Get Tips', Colors.orange)),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(child: _buildActionCard(context, Icons.water_drop, 'Hydration', Colors.cyan)),
                const SizedBox(width: 12),
                Expanded(child: _buildActionCard(context, Icons.wb_sunny, 'UV Check', Colors.amber)),
              ],
            ),
            const SizedBox(height: 20),
            const Text('Skin Health Score', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  children: [
                    CircularProgressIndicator(
                      value: 0.78,
                      strokeWidth: 8,
                      backgroundColor: Colors.grey[300],
                    ),
                    const SizedBox(width: 20),
                    const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('78/100', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                        Text('Good skin health!', style: TextStyle(color: Colors.green)),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionCard(BuildContext context, IconData icon, String label, Color color) {
    return Card(
      child: InkWell(
        onTap: () {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('$label tapped!'), duration: const Duration(seconds: 1)),
          );
        },
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              Icon(icon, size: 32, color: color),
              const SizedBox(height: 8),
              Text(label, style: const TextStyle(fontWeight: FontWeight.w500)),
            ],
          ),
        ),
      ),
    );
  }
}

class AnalysisPage extends StatefulWidget {
  const AnalysisPage({super.key});

  @override
  State<AnalysisPage> createState() => _AnalysisPageState();
}

class _AnalysisPageState extends State<AnalysisPage> {
  bool _isAnalyzing = false;
  bool _showResults = false;

  void _startAnalysis() {
    setState(() {
      _isAnalyzing = true;
      _showResults = false;
    });
    Future.delayed(const Duration(seconds: 3), () {
      setState(() {
        _isAnalyzing = false;
        _showResults = true;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Skin Analysis'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (!_isAnalyzing && !_showResults) ...[
                Icon(Icons.camera_alt, size: 80, color: Theme.of(context).colorScheme.primary),
                const SizedBox(height: 20),
                const Text('Ready to Analyze', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                const SizedBox(height: 10),
                const Text('Tap the button below to start skin analysis', textAlign: TextAlign.center),
                const SizedBox(height: 30),
                ElevatedButton.icon(
                  onPressed: _startAnalysis,
                  icon: const Icon(Icons.play_arrow),
                  label: const Text('Start Analysis'),
                  style: ElevatedButton.styleFrom(padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16)),
                ),
              ],
              if (_isAnalyzing) ...[
                const CircularProgressIndicator(),
                const SizedBox(height: 20),
                const Text('Analyzing your skin...', style: TextStyle(fontSize: 18)),
              ],
              if (_showResults) ...[
                const Icon(Icons.check_circle, size: 60, color: Colors.green),
                const SizedBox(height: 20),
                const Text('Analysis Complete!', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                const SizedBox(height: 20),
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: [
                        _buildResultRow('Hydration', '72%', Colors.blue),
                        _buildResultRow('Oiliness', '45%', Colors.orange),
                        _buildResultRow('Elasticity', '85%', Colors.green),
                        _buildResultRow('Pores', '38%', Colors.purple),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _showResults = false;
                    });
                  },
                  child: const Text('Analyze Again'),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildResultRow(String label, String value, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 16)),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
            decoration: BoxDecoration(color: color.withOpacity(0.2), borderRadius: BorderRadius.circular(12)),
            child: Text(value, style: TextStyle(color: color, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }
}

class HistoryPage extends StatelessWidget {
  const HistoryPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('History'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: 5,
        itemBuilder: (context, index) {
          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: Theme.of(context).colorScheme.primaryContainer,
                child: Text('${85 - index * 3}'),
              ),
              title: Text('Analysis ${5 - index}'),
              subtitle: Text('${index + 1} days ago'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Viewing analysis ${5 - index}'), duration: const Duration(seconds: 1)),
                );
              },
            ),
          );
        },
      ),
    );
  }
}

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const CircleAvatar(radius: 50, child: Icon(Icons.person, size: 50)),
            const SizedBox(height: 16),
            const Text('User', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            const Text('user@example.com'),
            const SizedBox(height: 24),
            _buildProfileOption(context, Icons.settings, 'Settings'),
            _buildProfileOption(context, Icons.notifications, 'Notifications'),
            _buildProfileOption(context, Icons.help, 'Help & Support'),
            _buildProfileOption(context, Icons.info, 'About'),
            _buildProfileOption(context, Icons.logout, 'Logout'),
          ],
        ),
      ),
    );
  }

  Widget _buildProfileOption(BuildContext context, IconData icon, String label) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Icon(icon),
        title: Text(label),
        trailing: const Icon(Icons.chevron_right),
        onTap: () {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('$label tapped!'), duration: const Duration(seconds: 1)),
          );
        },
      ),
    );
  }
}