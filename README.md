# caster-plugins
Plugins for Caster

## Keepass Plugin

*Warning: Not security vetted! If verbose logging is activated in Caster your passwords may be logged.*

You'll be prompted for your password during Caster startup.

In order to map Keepass entries to Caster write a line in the **notes** of the entry which looks like the following:
```
castervoice: <words to say>
```

After restarting Caster you can instruct Caster to type the entry's password by saying:
```
key pass <words to say>
```

### Configuration

```
plugins:
  config:
    caster_timoses.keepass:
      path: <keepass_db_path>
```


## Credits

* castervim
    * https://github.com/shippy/vim-grammar
    * https://github.com/davitenio/dragonfly-macros
