## bn

`bn` is an agent-friendly Binary Ninja CLI. It talks to a local Binary Ninja GUI plugin over a Unix domain socket instead of trying to run headless analysis in this environment.

### Install the companion plugin

```bash
uv run bn plugin install
```

That links [`plugin/bn_agent_bridge`](/Users/banteg/dev/banteg/bn/plugin/bn_agent_bridge) into the Binary Ninja plugins directory.

### Start using it

Open one or more binaries in the Binary Ninja GUI, then run:

```bash
uv run bn doctor
uv run bn target list
uv run bn function list
uv run bn decompile --target active sub_401000
```

Large results automatically spill to a cache artifact and print a compact JSON envelope with the artifact path.

### Mutation examples

```bash
uv run bn symbol rename --target 123:1:7 sub_401000 player_update --preview
uv run bn proto set --target 123:1:7 sub_401000 "int __cdecl player_update(Player* self)"
uv run bn local rename --target 123:1:7 sub_401000 var_14 speed
uv run bn struct field set --target 123:1:7 Player 0x308 movement_flag_selector uint32_t
uv run bn patch bytes --target 123:1:7 0x401000 "90 90" --preview
```

### Batch manifests

`bn batch apply manifest.json` expects a payload shaped like:

```json
{
  "target": "123:1:7",
  "preview": true,
  "ops": [
    {
      "op": "rename_symbol",
      "kind": "function",
      "identifier": "sub_401000",
      "new_name": "player_update"
    },
    {
      "op": "set_prototype",
      "identifier": "player_update",
      "prototype": "int __cdecl player_update(Player* self)"
    }
  ]
}
```
