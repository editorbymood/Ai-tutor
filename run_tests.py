"""
Comprehensive test runner script for AI-Powered Personal Tutor.

This script runs all tests and generates reports.
"""
import os
import sys
import subprocess
import argparse
from datetime import datetime


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {description} failed with error code {e.returncode}")
        return False


def run_unit_tests(args):
    """Run unit tests with pytest."""
    cmd = "pytest"
    
    if args.coverage:
        cmd += " --cov=apps --cov-report=html --cov-report=term"
    
    if args.verbose:
        cmd += " -v"
    
    if args.parallel:
        cmd += " -n auto"
    
    if args.markers:
        cmd += f" -m {args.markers}"
    
    if args.test_file:
        cmd += f" {args.test_file}"
    
    return run_command(cmd, "Unit Tests")


def run_integration_tests(args):
    """Run integration tests."""
    cmd = "pytest tests/integration/"
    
    if args.verbose:
        cmd += " -v"
    
    return run_command(cmd, "Integration Tests")


def run_load_tests(args):
    """Run load tests with Locust."""
    users = args.users or 100
    spawn_rate = args.spawn_rate or 10
    run_time = args.run_time or "5m"
    
    cmd = f"locust -f tests/load_test.py --host=http://localhost:8000 "
    cmd += f"--users {users} --spawn-rate {spawn_rate} --run-time {run_time} "
    cmd += "--headless --html=reports/load_test_report.html"
    
    return run_command(cmd, f"Load Tests ({users} users)")


def run_linting(args):
    """Run code linting."""
    commands = [
        ("flake8 apps/ backend/", "Flake8 Linting"),
        ("black --check apps/ backend/", "Black Code Formatting Check"),
        ("isort --check-only apps/ backend/", "Import Sorting Check"),
    ]
    
    results = []
    for cmd, desc in commands:
        results.append(run_command(cmd, desc))
    
    return all(results)


def run_security_checks(args):
    """Run security checks."""
    commands = [
        ("bandit -r apps/ backend/", "Bandit Security Check"),
        ("safety check", "Safety Dependency Check"),
    ]
    
    results = []
    for cmd, desc in commands:
        results.append(run_command(cmd, desc))
    
    return all(results)


def generate_report(results):
    """Generate test report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""
{'='*60}
TEST REPORT
{'='*60}
Generated: {timestamp}

Results:
"""
    
    for test_type, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        report += f"  {test_type}: {status}\n"
    
    report += f"\n{'='*60}\n"
    
    # Save report
    os.makedirs("reports", exist_ok=True)
    report_file = f"reports/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(report_file, "w") as f:
        f.write(report)
    
    print(report)
    print(f"Report saved to: {report_file}")
    
    return all(results.values())


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="Run tests for AI-Powered Personal Tutor")
    
    # Test selection
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--load", action="store_true", help="Run load tests")
    parser.add_argument("--lint", action="store_true", help="Run linting")
    parser.add_argument("--security", action="store_true", help="Run security checks")
    
    # Test options
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--parallel", "-n", action="store_true", help="Run tests in parallel")
    parser.add_argument("--markers", "-m", help="Run tests with specific markers")
    parser.add_argument("--test-file", help="Run specific test file")
    
    # Load test options
    parser.add_argument("--users", type=int, help="Number of users for load test")
    parser.add_argument("--spawn-rate", type=int, help="Spawn rate for load test")
    parser.add_argument("--run-time", help="Run time for load test (e.g., 5m, 1h)")
    
    args = parser.parse_args()
    
    # If no specific test selected, run all
    if not any([args.unit, args.integration, args.load, args.lint, args.security]):
        args.all = True
    
    results = {}
    
    print(f"\n{'='*60}")
    print("AI-POWERED PERSONAL TUTOR - TEST SUITE")
    print(f"{'='*60}\n")
    
    # Run selected tests
    if args.all or args.lint:
        results["Linting"] = run_linting(args)
    
    if args.all or args.security:
        results["Security Checks"] = run_security_checks(args)
    
    if args.all or args.unit:
        results["Unit Tests"] = run_unit_tests(args)
    
    if args.all or args.integration:
        results["Integration Tests"] = run_integration_tests(args)
    
    if args.load:
        results["Load Tests"] = run_load_tests(args)
    
    # Generate report
    all_passed = generate_report(results)
    
    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()