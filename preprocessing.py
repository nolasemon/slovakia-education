import pandas as pd
import numpy as np

TRANSLATE_COLUMNS = {'5-ročné vekové skupiny': 'year_5_age_groups',
                     'Ekonomické vekové skupiny': 'economical_age_groups',
                     'Kód kraja': 'NUTS3_CODE',
                     'Kód obce': 'LAU2_CODE',
                     'Kód oblasti': 'NUTS2_CODE',
                     'Kód okresu': 'LAU1_CODE',
                     'Kód štátu': 'NUTS1_CODE',
                     'Názov kraja': 'region_name',
                     'Názov obce': 'municipality_name',
                     'Názov oblasti': 'NUTS2_name',
                     'Názov okresu': 'district_name',
                     'Názov štátu': 'state_name',
                     'Odvetvie ekonomickej činnosti\u200b (NACE - sekcie)': 'NACE_section',
                     'Pohlavie': 'sex',
                     'Súčasná ekonomická aktivita': 'current_economic_activity',
                     'Vek': 'age',
                     'Vzdelanie': 'education',
                     'Zamestnanie '
                     '(ISCO - triedy)': 'ISCO_occupation',
                     'abs.': 'count'}

EDUCATION_CATEGORY_MAP = {
    "základné vzdelanie - 1. stupeň základnej školy": "primary",
    "základné vzdelanie (bližšie neuvedené)": "primary",
    "základné vzdelanie - 2. stupeň základnej školy": "primary",
    "úplné stredné vzdelanie s maturitou (bližšie neuvedené)": "secondary",
    "stredné odborné (učňovské) vzdelanie bez maturity a bez výučného listu (zaškolenie, zaučenie)": "secondary",
    "úplné stredné vzdelanie s maturitou odborné (učňovské) s výučným listom": "secondary",
    "stredné odborné (učňovské) vzdelanie bez maturity (bližšie neuvedené)": "secondary",
    "úplné stredné vzdelanie s maturitou odborné": "secondary",
    "stredné odborné (učňovské) vzdelanie bez maturity s výučným listom": "secondary",
    "stredné odborné (učňovské) vzdelanie bez maturity s vysvedčením o záverečnej skúške": "secondary",
    "úplné stredné vzdelanie s maturitou všeobecné": "secondary",
    "vyššie odborné vzdelanie vyššie odborné (absolventská skúška, absolventský diplom)": "vocational",
    "vyššie odborné vzdelanie nadstavbové (maturita absolventov učebných odborov stredných odborných škôl)": "vocational",
    "vyššie odborné vzdelanie pomaturitné (pomaturitné kvalifikačné)": "vocational",
    "vyššie odborné vzdelanie (bližšie neuvedené)": "vocational",
    "vysokoškolské vzdelanie - 1. stupeň (Bc.)": "higher",
    "vysokoškolské vzdelanie (bližšie neuvedené)": "higher",
    "vysokoškolské vzdelanie - 2. stupeň (Ing.; Mgr.; MUDr.; a i.)": "higher",
    "vysokoškolské vzdelanie - 3. stupeň (PhD.; a i.)": "higher",
    "bez ukončeného vzdelania – osoby vo veku 0-14 rokov": "without",
    "bez školského vzdelania – osoby vo veku 15 rokov a viac": "without",
    "nezistené": "unspecified",
    "dôverné": "unspecified",
}

ECONOMIC_SECTORS_MAP = {
    'nezistené': 'undefined',
    'Ostatné činnosti': 'other activities',
    'Poľnohospodárstvo, lesníctvo a rybolov': 'primary',
    'Ťažba a dobývanie': 'primary',
    'Stavebníctvo': 'secondary',
    'Priemyselná výroba': 'secondary',
    'Veľkoobchod a maloobchod; oprava motorových vozidiel a motocyklov': 'tertiary',
    'Doprava a skladovanie': 'tertiary',
    'Ubytovacie a stravovacie služby': 'tertiary',
    'Informácie a komunikácia': 'tertiary',
    'Činnosti v oblasti nehnuteľností': 'tertiary',
    'Odborné, vedecké a technické činnosti': 'tertiary',
    'Administratívne a podporné služby': 'tertiary',
    'Vzdelávanie': 'tertiary',
    'Umenie, zábava a rekreácia': 'tertiary',
    'Činnosti extrateritoriálnych organizácií a združení': 'tertiary',
    'Zdravotníctvo a sociálna pomoc': 'tertiary',
    'Dodávka elektriny, plynu, pary a studeného vzduchu': 'tertiary',
    'Finančné a poisťovacie činnosti': 'tertiary',
    'Dodávka vody; čistenie a odvod odpadových vôd, odpady a služby odstraňovania odpadov': 'tertiary',
    'Verejná správa a obrana; povinné sociálne zabezpečenie': 'tertiary',
    'Činnosti domácností ako zamestnávateľov; nediferencované činnosti v domácnostiach produkujúce tovary a služby na vlastné použitie': 'tertiary'
}

OCCUPATION_ISCO_MAP = {
    "Pracovníci v osobných službách": "Service workers and shop and market sales workers",
    "Odborní pracovníci v oblasti práva, sociálnych vecí a kultúry a podobní pracovníci": "Professionals",
    "Administratívni pracovníci v zákazníckych službách": "Clerks",
    "Riadiaci pracovníci (manažéri) vo výrobe a v špecializovaných službách": "Legislators, senior officials and managers",
    "Špecialisti v oblasti práva, sociálnych vecí a kultúry": "Professionals",
    "Administratívni pracovníci na záznam číselných a skladových údajov": "Clerks",
    "Predavači": "Service workers and shop and market sales workers",
    "Pracovníci pri likvidácii odpadu a ostatní nekvalifikovaní pracovníci": "Elementary occupations",
    "Riadiaci pracovníci (manažéri) v hotelových, reštauračných, obchodných a v ostatných službách": "Legislators, senior officials and managers",
    "Špecialisti v oblasti vedy a techniky": "Professionals",
    "Špecialisti v oblasti informačných a komunikačných technológií": "Professionals",
    "Kvalifikovaní robotníci v hutníctve, strojárstve a podobní robotníci": "Plant and machine operators and assemblers",
    "Montážni robotníci": "Plant and machine operators and assemblers",
    "Vodiči a obsluha pojazdných strojných zariadení": "Plant and machine operators and assemblers",
    "Technici v oblasti informačných a komunikačných technológií": "Technicians and associate professionals",
    "Elektrikári a elektronici": "Craft and related trades workers",
    "Riadiaci pracovníci (manažéri)  administratívnych, podporných a obchodných  činností": "Legislators, senior officials and managers",
    "Špecialisti administratívnych, podporných a obchodných činností": "Professionals",
    "Technici a odborní pracovníci v oblasti vedy a techniky": "Technicians and associate professionals",
    "Odborní pracovníci v zdravotníctve": "Professionals",
    "Odborní pracovníci administratívnych, podporných a obchodných činností": "Professionals",
    "Pracovníci v oblasti osobnej starostlivosti": "Service workers and shop and market sales workers",
    "Spracovatelia a výrobcovia potravinárskych výrobkov, výrobkov z dreva a odevov": "Craft and related trades workers",
    "Operátori stacionárnych strojov a zariadení": "Plant and machine operators and assemblers",
    "Všeobecní administratívni pracovníci a zapisovatelia": "Clerks",
    "Pracovníci verejnej ochrany a bezpečnostných služieb": "Service workers and shop and market sales workers",
    "Učitelia a odborní pedagogickí pracovníci": "Professionals",
    "Ostatní pomocní administratívni pracovníci": "Clerks",
    "Špecialisti v zdravotníctve": "Professionals",
    "Pomocní pracovníci v ťažbe, stavebníctve, výrobe a doprave": "Elementary occupations",
    "Pomocní pracovníci pri príprave jedla": "Elementary occupations",
    "Kvalifikovaní pracovníci v poľnohospodárstve (trhovo orientovaní)": "Skilled agricultural and fishery workers",
    "Zákonodarcovia, ústavní činitelia, vysokí štátni úradníci a najvyšší predstavitelia podnikov a organizácií": "Legislators, senior officials and managers",
    "Umeleckí a ruční remeselníci a tlačiari": "Craft and related trades workers",
    "Ostatné ozbrojené sily": "Armed forces",
    "Dôstojníci ozbrojených síl": "Armed forces",
    "Upratovači a pomocníci": "Elementary occupations",
    "Kvalifikovaní stavební robotníci a remeselníci okrem elektrikárov": "Craft and related trades workers",
    "Pomocní pracovníci v poľnohospodárstve, lesníctve a rybárstve": "Elementary occupations",
    "Poddôstojníci ozbrojených síl": "Armed forces",
    "Pouliční predavači a pomocní pracovníci v podobných  službách": "Service workers and shop and market sales workers",
    "Kvalifikovaní pracovníci v lesníctve, rybárstve a poľovníctve (trhovo orientovaní)": "Skilled agricultural and fishery workers",
    "Farmári, rybári, poľovníci a zberači úrody (samozásobovatelia)": "Skilled agricultural and fishery workers",
    "nezistené": "unspecified",
    "neaplikovateľné": "inapplicable"
}

TRANSLATE_SEX = {
    'muž': 'male',
    'žena': 'female'
}


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Translates names of columns from Slovak to English
    .. note:: This function doesn't translate entries in DataFrame

    :param df: DataFrame with Slovak names of columns
    :return: DataFrame with English names of columns
    """
    return df.rename(columns=TRANSLATE_COLUMNS)


def replace_with_nan(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replaces entries like "nezistené" with np.NaN
    :param df: DataFrame with string literals corresponding to NaN
    :return: DataFrame with NaN values
    """
    return df.replace(['nezistené', 'dôverné'], np.NaN)


def translate_sex(df: pd.DataFrame) -> pd.DataFrame:
    return df.replace(TRANSLATE_SEX)

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = rename_columns(df)
    df = translate_sex(df)
    if "age" in df:
        df["age"] = pd.to_numeric(df["age"].replace({"90 a viac rokov": "90"}))
    if "education" in df.columns:
        df["education_category"] = df["education"].map(EDUCATION_CATEGORY_MAP).astype('category')
    if "ISCO_occupation" in df.columns:
        df["ISCO_group"] = df["ISCO_occupation"].map(OCCUPATION_ISCO_MAP).astype('category')
    if "NACE_section" in df.columns:
        df['NACE_group'] = df['NACE_section'].map(ECONOMIC_SECTORS_MAP).astype('category')
    object_columns = [column for column in df.columns if df[column].dtype == 'object']
    df[object_columns] = df[object_columns].astype('string')
    df[object_columns] = df[object_columns].astype('category')
    return df