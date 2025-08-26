# Extensibility

SAPro exposes several extension points for feature modules:

- **Event listeners**: Use `sap.event_bus()` to subscribe to events using
  `subscribe(event, listener)` and respond when events are emitted.
- **Module registration**: Register new modules via `sap.register_module()` or
  the convenience helpers `sap.register_tax_module()` and
  `sap.register_payroll_module()`.
- **Configuration hooks**: Provide `custom_fields` and `validation_rules`
  through configuration and apply them with `sap.apply_hooks(config, bus)`.
