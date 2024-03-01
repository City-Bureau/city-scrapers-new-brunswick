from city_scrapers_core.spiders import CityScrapersSpider

from city_scrapers.mixins.middlesex_co import MiddlesexCoMixin  # Corrected import path

# Configuration for each spider
spider_configs = [
    {
        "class_name": "MiddlesexCoBoCCSpider",
        "name": "newbnj_middlesex_co_bocc",
        "agency": "Board of County Commissioners",
        "committee_id": 43,
    },
    {
        "class_name": "MiddlesexCoPBSpider",
        "name": "newbnj_middlesex_co_pb",
        "agency": "Planning Board (MCOP)",
        "committee_id": 34,
    },
    {
        "class_name": "MiddlesexCoDRCSpider",
        "name": "newbnj_middlesex_co_drc",
        "agency": "Development Review Committee (DRC)",
        "committee_id": 44,
    },
    {
        "class_name": "MiddlesexCoCADBSpider",
        "name": "newbnj_middlesex_co_cadb",
        "agency": "County Agriculture Development Board (CADB)",
        "committee_id": 2,
    },
    {
        "class_name": "MiddlesexCoWRASpider",
        "name": "newbnj_middlesex_co_wra",
        "agency": "Water Resources Association (WRA)",
        "committee_id": 45,
    },
    {
        "class_name": "MiddlesexCoEBSpider",
        "name": "newbnj_middlesex_co_eb",
        "agency": "Ethics Board",
        "committee_id": 10,
    },
    {
        "class_name": "MiddlesexCoWEaFOCSpider",
        "name": "newbnj_middlesex_co_weafoc",
        "agency": "WDB Executive and Fiscal Oversight Committee",
        "committee_id": 58,
    },
    {
        "class_name": "MiddlesexCoCBoASpider",
        "name": "newbnj_middlesex_co_cboa",
        "agency": "Construction Board of Appeals",
        "committee_id": 6,
    },
    {
        "class_name": "MiddlesexCoWDBSpider",
        "name": "newbnj_middlesex_co_wdb",
        "agency": "Workforce Development Board",
        "committee_id": 42,
    },
    {
        "class_name": "MiddlesexCoMSpider",
        "name": "newbnj_middlesex_co_m",
        "agency": "MCIA",
        "committee_id": 28,
    },
    {
        "class_name": "MiddlesexCoBoESpider",
        "name": "newbnj_middlesex_co_boe",
        "agency": "Board of Elections",
        "committee_id": 9,
    },
    {
        "class_name": "MiddlesexCoJHIFCSpider",
        "name": "newbnj_middlesex_co_jhifc",
        "agency": "Middlesex County Joint Health Insurance Fund Commission",
        "committee_id": 20,
    },
    {
        "class_name": "MiddlesexCoTBSpider",
        "name": "newbnj_middlesex_co_tb",
        "agency": "TAX BOARD",
        "committee_id": 38,
    },
    {
        "class_name": "MiddlesexCoICSpider",
        "name": "newbnj_middlesex_co_ic",
        "agency": "Middlesex County Insurance Commission",
        "committee_id": 52,
    },
    {
        "class_name": "MiddlesexCoWMPAPHSpider",
        "name": "newbnj_middlesex_co_wmpaph",
        "agency": "Wastewater Management Plan Amendment Public Hearings",
        "committee_id": 47,
    },
    {
        "class_name": "MiddlesexCoWOSCSpider",
        "name": "newbnj_middlesex_co_wosc",
        "agency": "WDB One Stop Committee",
        "committee_id": 48,
    },
    {
        "class_name": "MiddlesexCoSWACSpider",
        "name": "newbnj_middlesex_co_swac",
        "agency": "Solid Waste Advisory Council (SWAC)",
        "committee_id": 36,
    },
    {
        "class_name": "MiddlesexCoSWMPHSpider",
        "name": "newbnj_middlesex_co_swmph",
        "agency": "Solid Waste Management Public Hearings",
        "committee_id": 57,
    },
    {
        "class_name": "MiddlesexCoCoCAaMCSpider",
        "name": "newbnj_middlesex_co_cocaamc",
        "agency": "Commission on Child Abuse and Missing Children",
        "committee_id": 5,
    },
    {
        "class_name": "MiddlesexCoCfCSSpider",
        "name": "newbnj_middlesex_co_cfcs",
        "agency": "Council for Children's Services",
        "committee_id": 7,
    },
    {
        "class_name": "MiddlesexCoHTFABSpider",
        "name": "newbnj_middlesex_co_htfab",
        "agency": "Homeless Trust Fund Advisory Board",
        "committee_id": 55,
    },
    {
        "class_name": "MiddlesexCoHSACSpider",
        "name": "newbnj_middlesex_co_hsac",
        "agency": "Human Services Advisory Council",
        "committee_id": 15,
    },
    {
        "class_name": "MiddlesexCoLACfAaDASpider",
        "name": "newbnj_middlesex_co_lacfaada",
        "agency": "Local Advisory Commission for Alcoholism and Drug Abuse",
        "committee_id": 18,
    },
    {
        "class_name": "MiddlesexCoMHBSpider",
        "name": "newbnj_middlesex_co_mhb",
        "agency": "Mental Health Board",
        "committee_id": 25,
    },
    {
        "class_name": "MiddlesexCoHCoCCSpider",
        "name": "newbnj_middlesex_co_hcocc",
        "agency": "Middlesex County Housing Continuum of Care Committee",
        "committee_id": 54,
    },
    {
        "class_name": "MiddlesexCoOoA&DSSpider",
        "name": "newbnj_middlesex_co_ooa&ds",
        "agency": "Middlesex County Office of Aging & Disabled Services",
        "committee_id": 59,
    },
    {
        "class_name": "MiddlesexCoRWACSpider",
        "name": "newbnj_middlesex_co_rwac",
        "agency": "Ryan White Advisory Council",
        "committee_id": 53,
    },
    {
        "class_name": "MiddlesexCoVASpider",
        "name": "newbnj_middlesex_co_va",
        "agency": "Veterans' Advisory",
        "committee_id": 40,
    },
]


def create_spiders():
    """
    Dynamically create spider classes using the spider_configs list
    and then register them in the global namespace. This approach
    is the equivalent of declaring each spider class in the same
    file but it is a little more concise.
    """
    for config in spider_configs:
        # Using config['class_name'] to dynamically define the class name
        class_name = config.pop(
            "class_name"
        )  # Remove class_name from config to avoid conflicts
        # We make sure that the class_name is not already in the global namespace
        # Because some scrapy CLI commands like `scrapy list` will inadvertently
        # declare the spider class more than once otherwise
        if class_name not in globals():
            spider_class = type(
                class_name,
                (MiddlesexCoMixin, CityScrapersSpider),  # Base classes
                {**config},  # Attributes including name, agency, committee_id
            )

            # Register the class in the global namespace using its class_name
            globals()[class_name] = spider_class


# Call the function to create spiders
create_spiders()
