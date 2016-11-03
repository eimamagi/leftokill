import ConfigParser

def parse_config(conffile, logger):
    reqsections = set(['general', 'report'])
    confopts = dict()

    try:
        config = ConfigParser.ConfigParser()
        if config.read(conffile):
            sections = map(lambda v: v.lower(), config.sections())

            diff = reqsections.difference(sections)
            if diff:
                raise ConfigParser.NoSectionError((' '.join(diff)))

            for section in config.sections():
                if section.startswith('General'):
                    confopts['killeverysec'] = float(config.get(section, 'KillEverySec'))
                    confopts['noexec'] = eval(config.get(section, 'NoExecute'))
                    val = config.get(section, 'LogMode')
                    if ',' in val:
                        confopts['logmode'] = map(lambda v: v.strip(), val.split(','))
                    else:
                        confopts['logmode'] = [val.strip()]
                if section.startswith('Report'):
                    confopts['sendreport'] = eval(config.get(section, 'Send'))
                    confopts['reportto'] = config.get(section, 'To')
                    confopts['reportfrom'] = config.get(section, 'From')
                    confopts['reportsmtp'] = config.get(section, 'SMTP')
                    confopts['reportsmtplogin'] = config.get(section, 'SMTPLogin')
                    confopts['reportsmtppass'] = config.get(section, 'SMTPPass')
                    confopts['reporteveryhour'] = 3600 * float(config.get(section, 'EveryHours'))
                    confopts['verbose'] = eval(config.get(section, 'Verbose'))
        else:
            logger.error('Missing %s' % conffile)
            raise SystemExit(1)

    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as e:
        logger.error(e)
        raise SystemExit(1)

    except (ConfigParser.MissingSectionHeaderError, SystemExit) as e:
        if getattr(e, 'filename', False):
            logger.error(e.filename + ' is not a valid configuration file')
            logger.error(e.message)
        raise SystemExit(1)

    return confopts