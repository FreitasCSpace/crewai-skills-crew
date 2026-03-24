# Skill: flutter

## Purpose
Build, test, and manage Flutter/Dart mobile & web applications.

## When to use
- Creating new Flutter projects or adding features
- Building and running Flutter apps (iOS, Android, Web)
- Managing packages (pub), assets, and dependencies
- Running tests and analyzing code
- Generating code (build_runner, freezed, json_serializable)

## Prerequisites
- Flutter SDK installed: `brew install --cask flutter` or from https://flutter.dev
- Verify: `flutter doctor`

## How to execute

**Check environment:**
```bash
flutter doctor -v
```

**Create a new project:**
```bash
flutter create --org com.example --platforms android,ios,web my_app
cd my_app
```

**Run the app:**
```bash
# List available devices
flutter devices

# Run on a specific device
flutter run -d chrome          # Web
flutter run -d macos           # macOS desktop
flutter run -d DEVICE_ID       # Specific device
```

**Build for release:**
```bash
# Android APK
flutter build apk --release

# Android App Bundle (Play Store)
flutter build appbundle --release

# iOS
flutter build ios --release

# Web
flutter build web --release
```

**Manage dependencies:**
```bash
# Add a package
flutter pub add http
flutter pub add provider
flutter pub add go_router
flutter pub add flutter_bloc

# Add dev dependency
flutter pub add --dev build_runner
flutter pub add --dev json_serializable

# Get/upgrade all packages
flutter pub get
flutter pub upgrade
```

**Create a new widget/screen:**
```bash
cat > lib/screens/home_screen.dart << 'EOF'
import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Home')),
      body: const Center(child: Text('Hello Flutter!')),
    );
  }
}
EOF
```

**Create a StatefulWidget:**
```bash
cat > lib/widgets/counter_widget.dart << 'EOF'
import 'package:flutter/material.dart';

class CounterWidget extends StatefulWidget {
  const CounterWidget({super.key});

  @override
  State<CounterWidget> createState() => _CounterWidgetState();
}

class _CounterWidgetState extends State<CounterWidget> {
  int _count = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text('Count: $_count', style: Theme.of(context).textTheme.headlineMedium),
        const SizedBox(height: 16),
        ElevatedButton(
          onPressed: () => setState(() => _count++),
          child: const Text('Increment'),
        ),
      ],
    );
  }
}
EOF
```

**Create a data model with JSON serialization:**
```bash
cat > lib/models/user.dart << 'EOF'
import 'package:json_annotation/json_annotation.dart';
part 'user.g.dart';

@JsonSerializable()
class User {
  final int id;
  final String name;
  final String email;

  User({required this.id, required this.name, required this.email});

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
EOF

# Generate the .g.dart file
dart run build_runner build --delete-conflicting-outputs
```

**Run tests:**
```bash
# All tests
flutter test

# Specific test file
flutter test test/widget_test.dart

# With coverage
flutter test --coverage
```

**Analyze code:**
```bash
flutter analyze
dart format lib/ --set-exit-if-changed
```

**Clean and rebuild:**
```bash
flutter clean && flutter pub get
```

**Generate platform-specific files:**
```bash
# Regenerate platform folders
flutter create --platforms android,ios .

# Update app icon (using flutter_launcher_icons package)
flutter pub add --dev flutter_launcher_icons
dart run flutter_launcher_icons
```

## Output contract
- stdout: build output, test results, or generated files
- exit_code 0: success
- exit_code 1+: build error, test failure, or analysis issue

## Evaluate output
If build fails: read the error — usually a missing import, type mismatch, or null safety issue.
If `flutter doctor` shows issues: fix them before building.
Always run `flutter analyze` before committing to catch lint issues.
