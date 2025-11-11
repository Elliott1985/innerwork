from app import create_app

app = create_app()

print("\n=== Checking Stripe Routes ===")
print("\nAll registered routes:")
stripe_found = False
for rule in app.url_map.iter_rules():
    rule_str = str(rule)
    if 'stripe' in rule_str or 'purchase' in rule_str:
        print(f"✓ {rule.methods} {rule.rule} -> {rule.endpoint}")
        stripe_found = True

if not stripe_found:
    print("❌ No stripe routes found!")
else:
    print("\n✓ Stripe routes are registered")

print("\n=== Registered Blueprints ===")
for name, bp in app.blueprints.items():
    print(f"  - {name}: {bp.url_prefix}")
