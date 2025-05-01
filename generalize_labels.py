import re

GENERALIZATION_RULES = {
    "indoor": [
        "bedroom", "indoor", "art_gallery", "kitchen", "bathroom", "office", "room", "corridor", "hallway", "library",
        "museum", "buffet", "laboratorywet", "lyceum", "rotisserie", "saloon", "snack_bar", "student_center",
        "pantry", "parlor", "portrait_studio", "reception", "restaurant", "restaurant_patio", "shed",
        "shopfront", "shower", "staircase", "student_residence", "subway_interior", "supermarket",
        "television_studio", "ticket_booth", "videostore", "wet_bar", "window_seat", "barrel_storage",
        "bottle_storage", "witness_stand", "workshop", "confessional", "lobby", "martial_arts_gym",
        "military_hospital", "morgue", "music_studio", "nursery", "orchestra_pit", "shelter", "stall",
        "home_theater", "jail_cell", "jury_box", "dinette_home", "funeral_chapel", "galley", "food_court",
        "misc", "ballet", "bubble_chamber", "cellar", "cocktail_lounge", "dance_floor", "dining_area",
        "fireplace", "flatlet", "head_shop", "insane_asylum", "juke_joint", "loge", "lower_deck",
        "science_laboratory", "scullery", "store", "study_hall", "salonsanatorium", "open-hearth_furnace",
        "mess_hall", "mezzanine", "military_tent", "mobile_home", "motel", "nightclub", "nunnery",
        "nursing_home", "observatory_post", "optician", "organ_loft_interior", "orlop_deck", "ossuary",
        "oyster_bar", "assembly_hall", "awning_deck", "backdrop", "bric-a-brac", "salon", "sanatorium",
        "supply_chamber", "tannery", "threshing_floor", "tract_housing", "upper_balcony", "vestibule",
        "walkway", "pawnshop", "penalty_box", "pet_shop", "phone_booth", "physics_laboratory", "pizzeria",
        "police_station", "print_shop", "priory", "promenade", "promenade_deck", "pulpit", "refectory",
        "repair_shop", "residential_neighborhood", "resort", "scriptorium", "security_check_point",
        "shrine", "ski_lodge", "strip_mall", "submarine_interior", "sun_deck", "sushi_bar", "teashop",
        "thriftshop", "trading_floor", "station", "turkish_bath", "van_interior", "ventilation_shaft",
        "vestry", "voting_booth", "whispering_gallery", "widows_walk_interior", "winery", "hearth",
        "booth", "hotel_breakfast_area", "backseat", "departure_lounge", "balcony_interior", "machine_shop",
        "discotheque", "atrium_home", "attic", "bullpen", "particle_accelerator", "dining_hall", "bindery",
        "cafeteria", "fire_escape", "delicatessen", "dress_shop", "berth", "cybercafe", "anechoic_chamber",
        "hospital", "call_center", "exhibition_hall", "hatchery", "great_hall", "funeral_home", "arcade",
        "choir_loft_interior", "maternity_ward", "biology_laboratory", "backstage", "canteen", "imaret",
        "beer_hall", "conference_hall", "burial_chamber", "rectory", "igloo", "cheese_factory",
        "box_seat", "limousine_interior", "closet", "checkout_counter", "banquet_hall", "gazebo_interior",
        "nook", "conference_center", "airlock", "chapel", "basilica", "bank_vault", "bookbindery",
        "crawl_space", "cockpit", "chemistry_lab", "atrium_public", "legislative_chamber", "basement",
        "distillery", "covered_bridge_interior", "poop_deck", "coffee_shop", "entrance_hall",
        "greengrocery", "assembly_line", "entrance", "aquatic_theater", "belfry",  'recreation_room', 'hospital_room', 'cathedral_indoor', 'diner_indoor', 
        'warehouse_indoor', 'backstairs_indoor', 'restaurant_kitchen', 'cloister_indoor', 
        'oil_refinery_indoor', 'bus_station_indoor', 'velodrome_indoor', 'flea_market_indoor', 
        'brewing_indoor', 'labyrinth_indoor', 'church_indoor', 'dairy_indoor', 'escalator_indoor', 
        'lido_deck_indoor', 'bus_depot_indoor', 'reading_room', 'powder_room', 'pilothouse_indoor', 
        'jacuzzi_indoor', 'operating_room', 'museum_indoor', 'brickyard_indoor', 'synagogue_indoor', 
        'locker_room', 'gun_deck_indoor', 'ice_skating_rink_indoor', 'lab_classroom', 'batting_cage_indoor', 
        'reception_room', 'market_indoor', 'waiting_room', 'restroom_indoor', 'gymnasium_indoor', 
        'volleyball_court_indoor', 'car_dealership', 'ice_skating_rink_indoor', 'convenience_store_indoor', 
        'roundhouse', 'train_interior', 'train_interior', 'firing_range_indoor', 'bathroom_indoor',
        'desk_indoor', 'jail_indoor', 'locker_room_indoor', 'game_room_indoor', 'cinema_indoor',
        'kitchen_indoor', 'warehouse_indoor', 'casino_indoor', 'entertainment_indoor', 
        'server_room', 'mosque_indoor', 'monastery_indoor', 'inn_indoor', 'hot_tub_indoor', 
        'ticket_window_indoor', 'basketball_court_indoor', 'florist_shop_indoor', 'clean_room', 
        'elevated_catwalk', 'war_room', 'bunk_bed', 
        'pizzeria_indoor', 'darkroom', 'planetarium_indoor', 'kindergarden_classroom', 'newsstand_indoor', 
        'auto_mechanics_indoor', 'mental_institution_indoor', 'chicken_farm_indoor', 'baptistry_indoor', 
        'joss_house', 'tobacco_shop_indoor', 'bicycle_racks', 'athletic_field_indoor', 'amusement_arcade', 
        'palace_hall', 'steel_mill_indoor', 'newsroom', 'conference_room', 'batting_cage_indoor', 
        'chicken_coop_indoor', 'hutment', 'field_house', 'library_indoor', 'throne_room', 'control_room', 
        'cavern_indoor', 'bath_indoor', 'cabin_indoor', 'parking_garage_indoor', 'control_tower_indoor', 
        'dorm_room', 'game_room', 'water_park', 'tent_indoor', 'workroom', 'amusement_park', 'guardhouse', 
        'general_store_indoor', 'podium_indoor', 'water_treatment_plant_indoor', 'observatory_indoor', 'classroom', 
        'elevator_interior', 'tennis_court_indoor', 'kiosk_indoor', 'cargo_container_interior', 'living_room', 
        'bow_window_indoor', 'driving_range_indoor', 'schoolhouse', 'cargo_deck', 'quonset_hut_indoor', 'quonset_hut_outdoor',
        'museum_indoor', 'stateroom', 'geodesic_dome_indoor', 'lumberyard_indoor',  'bazaar_indoor', 
        'movie_theater_indoor', 'breakroom', 'manufactured_home', 'music_store', 'furnace_room', 
        'chair_lift', 'bicycle_racks', 'manual_labor',
        'outhouse_indoor', 'stage_indoor', 'television_room', 'indoor_seats', 'brewery_indoor', 'indoor_round', 
        'swimming_pool_indoor', 'nuclear_power_plant_indoor', 'packaging_plant', 'tearoom', 'kennel_indoor', 
        'entranceway_indoor', 'home_office', 'arrival_gate_indoor', 'bookshelf', 'guardroom',  
        'fitting_room_interior', 'bleachers_indoor', 'breakfast_table', 'hangar_indoor', 'computer_room', 
        'mental_institution_indoor', 'carport_indoor', 'pedestrian_overpass_indoor', 'incinerator_indoor', 
        'skywalk_indoor', 'bomb_shelter_indoor', 'pub_indoor', 'bistro_indoor', 'zen_garden', 'garage_indoor', 
        'greenhouse_indoor', 'hotel_room', 'apse_indoor', 'deck-house_deck_house', 'backroom', 'playroom', 
        'dining_room', 'lookout_station_indoor', 'bomb_shelter_indoor', 'courtroom', 'editing_room', 'sunroom', 
        'washhouse_indoor', 'patio_indoor', 'party_tent_indoor', 'bank_indoor', 'elevator_lobby', 'clock_tower_indoor', 'elevator_shaft', 'museum_outdoor', 
        'widows_walk_indoor',  'kitchenette', 'ballroom', 'mini_golf_course_indoor', 'science_museum', 
        'shipping_room', 'foundry_indoor','field_tent_indoor', 'fastfood_restaurant', 
        'circus_tent_indoor', 'engine_room', 'washhouse_indoor', 'road_indoor', 'childs_room',
        'flume_indoor', 'badminton_court_indoor', 'dressing_room','cardroom', 'indoor_procenium', 'operating_table', 'mineral_bath', 'lavatory',
        'factory_indoor','roller_skating_rink_indoor','amphitheater_indoor','hunting_lodge_indoor','lookout_station_indoor', 'doorway_indoor',
    ],
    "outdoor": [
        "outdoor", "landscape", 'greenhouse_outdoor', "garden", "road", "plaza", "city", "street", "park", "badlands",
        "back_porch", "bridle_path", "corner", "housing_project", "parade_ground", "patio", "playground",
        "raceway", "ranch", "roof", "rope_bridge", "roundabout", "runway", "sandbar", "slum",
        "t-bar_lift", "veranda", "viaduct", "yard", "airport_terminal", "boardwalk", "landing_deck",
        "revolving_door", "sand_trap", "wild", "gate", "scrubland", "block", "moon_bounce", "cabana",
        "hardware_store", "fairway",'brewery_outdoor', "chuck_wagon", "highway", "hoodoo", "hut", "lagoon", "lean-to",
        "loading_dock", "glade", "golf_course", "granary", "hacienda", "harbor", "hayloft", "hedgerow",
        "dolmen", "downtown", "driveway", "dugout", "farm", "fence", "forest_path", "fortress",
        "fountain", "gas_station", "embassy", "excavation", "exterior", "backwoods", "barbeque",'escalator_outdoor', 'bow_window_outdoor',
        "diving_board", "embrasure",'backstage_outdoor','bathhouse_outdoor',  "feed_bunk", "fire_trench", "floating_dock", "forecourt",
        "front_porch", "gas_well", "grape_arbor", "housing_estate", "inlet", "jungle", "kraal",
        "landing_strip", "layby", "meadow", "military_headquarters", "observation_station", "palestra",
        "pavement", "pinetum", "rest_stop", "shrubbery", "sidewalk", "snowbank", "outside", "glen", 'florist_shop_outdoor',
        "grove", "mesa", "mission", "pagoda", "platform", "porch", "portico", "postern", "quadrangle",
        "racecourse", "ramp", "rock_arch", "ruin", "seawall", "spillway", "stone_circle", "taxistand",
        "trench", "trestle_bridge", "village", "wave", "wharf", "zoo", "campus", "castle", "cemetery",
        "alley", "crosswalk", "dock", "landing", "picnic_area", "bridge", "freeway", "ski_jump",
        "jetty", "garbage_dump", "putting_green", "rest_area", "dam", "lock_chamber", "traffic_island",
        "chaparral", "raft", "rodeo", "landfill", "bog", "pueblo", "millrace", "levee", "canyon",
        "grotto", "crevasse", "campsite", "dirt_track", "mews", "embankment",  'firing_range_outdoor',
        "ditch", "fort", "youth_hostel", "megalith", "corral", "windstorm", "tower", "junk_pile",
        "menhir", "backstairs", "ditch", "fort", "youth_hostel", "megalith", "corral", "windstorm", 
        "tower", "junk_pile", "menhir", "backstairs", 'baptistry_outdoor', 'lighthouse', 'beer_garden', 'sandbox', 'circus_tent_outdoor', 
        'nuclear_power_plant_outdoor', 'lido_deck_outdoor', 'arrival_gate_outdoor', 'incinerator_outdoor', 
        'observatory_outdoor', 'train_station_outdoor', 'pub_outdoor', 'hunting_lodge_outdoor', 'lido_deck_outdoor', 
        'swimming_pool_outdoor', 'swimming_pool_outdoor', 'public_gardens', 'mansion', 'poolhouse', 
        'shelter_tent', 'wrestling_ring_outdoor', 'stadium_outdoor', 'football_field', 'courtyard', 
        'mini_golf_course_outdoor', 'tree_farm', 'hotel_outdoor', 
        'amphitheater', 'shopping_mall_outdoor', 'bazaar_outdoor', 'safari_park', 'road_cut', 'hazard_outdoor',
        'herb_garden', 'berth_deck', 'dairy_outdoor', 'rail_outdoor', 'mini_golf_course_outdoor', 
        'nuclear_power_plant_outdoor', 'monastery_outdoor', 'storm_cellar', 'apartment_building_outdoor', 
        'access_road', 'desert_road', 'country_road', 'bathhouse', 'factory_outdoor', 'florist_shop_outdoor', 
        'cottage_garden', 'mountain_snowy', 'estaminet', 'bell_foundry', 'ranch_house', 'barn', 
        'basketball_court_outdoor', 'field_road', 'piste_road', 'sporting_goods_store', 'field_tent_outdoor', 
        'garage_outdoor', 'roof_garden', 'booth_outdoor', 'planetarium_outdoor', 'outhouse_outdoor', 'chicken_coop_outdoor', 
        'washhouse_outdoor', 'church_outdoor', 'drugstore', 'roller_skating_rink_outdoor', 'bedchamber', 'archaeological_excavation', 
        'massage_room', 'auto_mechanics_outdoor', 'junkyard', 'pizzeria_outdoor', 'boathouse', 'hot_tub_outdoor', 
        'deck-house_boat_deck_house', 'dry_dock', 'steel_mill_outdoor', 'performance', 'dining_car', 'general_store_outdoor', 
        'botanical_garden', 'lean-to_tent', 'joss_house', 'fish_farm', 'poolroom_home', 'quonset_hut_outdoor', 'kennel_outdoor', 
        'amusement_park', 'cabins_outdoor',  'field_house', 'one-way_street', 'oil_refinery_outdoor', 
        'diner_outdoor', 'cavern_outdoor', 'control_tower_outdoor', 'mosque_outdoor', 'town_house', 'bus_depot_outdoor', 
        'water_park', 'water_gate', 'mountain_path', 'jacuzzi_outdoor', 'military_hut', 'hillock', 'quicksand', 
        'ice_shelf', 'lumberyard_outdoor', 'beach_house', 'strip_mine', 'gymnasium_outdoor',  
         'tree_house',  'assembly_plant',
        'kiosk_outdoor', 'gun_deck_outdoor', 'building_facade', 'bus_station_outdoor', 'shipyard_outdoor', 'bus_shelter', 
        'veterinarians_office', 'farmhouse', 'brickyard_outdoor', 'parkway', 'shelter_deck', 'byroad', 'guardroom', 
        'cathedral_outdoor', 'shower_room', 'movie_theater_outdoor', 'mineshaft', 'oyster_farm', 'loggia_outdoor', 
        'entranceway_outdoor', 'nursing_home_outdoor', 'warehouse_outdoor', 'mental_institution_outdoor', 'farm_building', 
        'hangar_outdoor', 'driving_range_outdoor', 'convenience_store_outdoor', 'lookout_station_outdoor', 
        'natural_history_museum', 'meat_house', 'tent_outdoor', 'carrousel', 'chicken_farm_outdoor', 'cloister_outdoor', 
        'starting_gate', 'labyrinth_outdoor', 'steam_plant_outdoor', 'skywalk_outdoor', 'bank_outdoor', 'party_tent_outdoor', 
        'bistro_outdoor', 'casino_outdoor', 'flowerbed', 'outbuilding', 'entryway_outdoor', 
        'inn_outdoor',  'utility_room', 'stable', 'dentists_office', 
        'podium_outdoor', 'bath_outdoor', 'railway_yard','sewing_room',  'cabin_outdoor', 
        'restroom_outdoor', 'terrace_farm', 'day_care_center', 'barndoor', 'schoolyard', 'lecture_room', 'foothill', 
        'floating_dry_dock', 'building_complex', 'auto_showroom', 'synagogue_outdoor', 
        'electrical_substation', 'library_outdoor', 'pilothouse_outdoor', 'teahouse', 'formal_garden', 'archaelogical_excavation', 
        'doorway_outdoor', 'track_outdoor', 'carport_outdoor', 'courthouse', 'apse_outdoor', 'ice_cream_parlor', 'manhole', 
        'parking_garage_outdoor', 'sunroom', 'root_cellar', 'oast_house', 'parking_lot', 'mens_store_outdoor', 'hen_yard', 
        'washroom', 'market_outdoor', 'tiltyard', 'country_house', 'boat_deck', 'plantation_house', 'stage_outdoor', 
        'newsstand_outdoor', 'coast_road', 'jail_outdoor', 'velodrome_outdoor', 'bleachers_outdoor', 'butchers_shop', 
        'flea_market_outdoor', 'basin_outdoor', 'geodesic_dome_outdoor', 'bowling_alley', 'science_museum', 'pawnshop_outdoor', 
        'fastfood_restaurant', 'root_cellar','foreshore', 'trailer_park', 'barnyard', 'pig_farm'

    ],
    "nature": [
        "broadleaf", "tree", "plant", "sky", "mountain", "lake", "river", "grass", "natural", "hill",
        "desert", "oasis", "ocean", "seaside", "shore", "tidal_basin", "wetland", "pasture", "vineyard",
        "valley", "wheat_field", "water_fountain", "snowfield", "sand", "marsh", "ocean_deep", "coast",
        "outcropping", "swimming_hole", "water_mill", "water_tower", "wind_farm", "dry", "flood_plain",
        "vinery", "beach", "ice_floe", "iceberg", "irrigation_ditch", "fjord", "flood", "fishpond",
        "cultivated", "nature", "jungle", "meadow", "inlet", "shrubbery", "snowbank", "pinetum", "moor",
        "mudflat", "orchard", "rainforest", "savanna", "salt_plain", "sea_cliff", "sinkhole", "swamp",
        "tundra", "water", "waterscape", "waterway", "watering_hole", "volcano", "cascade", "cataract",
        "plunge", "coral_reef", "woodland", "bay", "bottomland", "brooklet", "creek", "gorge", "glacier",
        "heath", "gulch", "butte", "estuary", "pond", "hot_spring", "hollow", "lava_flow", "bamboo_forest",
        "preserve", "canyon", "forest_fire", "vegetation", "rice_paddy", "hayfield", "cliff", "islet",
        "millpond", "corn_field", "lawn", "hedge_maze", "megalith", "ditch",'tea_garden',
        'mountain_road', 'bayou', 'semidesert', 'escarpment', 'forest_road', 'tidal_river', 
        'ocean_shallow', 'nature_preserve''mountain_road', 'bayou', 'semidesert', 'escarpment', 
        'forest_road', 'tidal_river', 'ocean_shallow', 'nature_preserve', 'rift_valley', 'barrack', 
        'herb_garden', 'mountain_snowy', 'vegetable_garden', 'japanese_garden', 'topiary_garden', 
        'cottage_garden', 'rock_garden', 'natural_spring', 'natural_spring'
    ],
    "people": [
        "person", "people", "man", "woman", "child", "crowd", "group", 'people', 'in_person', 'performance', 'crowd', 'social_event'
    ],
    "buildings": [
        "building", "buildings", "house", "structure", "architecture", "skyscraper", "acropolis", "catacomb",
        "palace", "mausoleum", "tomb", "sawmill", "sacristy", "mine", "embassy", "fire_station",
        "fortress", "granary", "funeral_chapel", "science_laboratory", "insane_asylum", 'jail_outdoor',
        "military_headquarters", "housing_estate", "medina", "naval_base", "nursing_home",
        "observatory_post", "paper_mill", "pavilion", "pier", "print_shop", "priory", "refectory",
        "residential_neighborhood", "resort", "sanatorium", "sugar_refinery", "scriptorium",
        "shrine", "station", "strip_mall", "warehouse", "winery", "abbey", "airport", "amphitheater",
        "aquarium", "archive", "art_school", "artists_loft", "auditorium", "auto_factory", "bar",
        "barbershop", "beauty_salon", "donjon", "mastaba", "mesoamerican", "rolling_mill",
        "cottage", "industrial_area", "army_base", "air_base", "armory", "dance_school", "loft",
        "bindery", "hospital", "kasbah", "funeral_home", "conference_center", "cheese_factory", 'customhouse', 'mansard',
        "call_center", "beer_hall", "fishmarket", "gasworks", "chalet", "chapel", "basilica", 'factory_outdoor',  
        "shop", "ziggurat", "oilrig", "dacha", "watchtower", 'caravansary', 'office_building', 'office_cubicles', 'warehouse_indoor', 'church_indoor', 'warehouse_indoor', 
        'department_store', 'candy_store', 'guesthouse', "gatehouse",'theater_outdoor', 'department_store', 'ranch_house', 'barn', 'chicken_coop_outdoor', 'field_house', 'control_room', 'general_store_outdoor', 'schoolhouse'
    ],
    "transport": [
        "car", "bus", "bicycle", "vehicle", "train", "truck", "motorcycle", "airplane", "boat", "taxiway",
        "runway", "t-bar_lift", "rope_bridge", "viaduct", "subway_interior",
        "signal_box", "ski_resort", "weighbridge", "highway", "lift_bridge", "loading_dock",
        "driveway", "freight_elevator", "gangplank", "bypass", "floating_dock", "landing_strip",
        "layby", "luggage_van", "rest_stop", "observation_station", "pumping_station", "airfield",
        "airport", "airport_ticket_counter", "baggage_claim", "cabin_cruiser", "pontoon_bridge",
        "taxistand", "van_interior", "platform", "station", "walkway", "overpass", "tollbooth",
        "air_base", "bridge", "jetty", "fly_bridge", "cockpit", "heliport", "passenger_deck",
        "box_seat", "backseat", "frontseat", "oilrig", "drill_rig", 'cargo_helicopter', 'train_station_outdoor', 'ferryboat_indoor', 'train_interior', 'train_railway', 
        'airplane_cabin', 'ferryboat_indoor', 'auto_mechanics_outdoor', 'rail_indoor', 'bus_interior', 'cargo_deck', 'cargo_container_interior', 'truck_stop', 'railroad_track', 
        'aircraft_carrier_object'
    ],
    "objects": [
        "furniture", "sofa", "chair", "table", "bed", "tv", "screen", "lamp", "cabinet", "mirror",
        "shelf", "fan", "freight_elevator", "walk_in_freezer", "laundromat", "fountain", "bubble_chamber",
        "fireplace", "open-hearth_furnace", "ball_pit", "batters_box", "bench", "door", "forklift",
        "vat", "arch", "pitchers_mound", "bullpen", "hatchery", "trellis", "alcove", "battlement",
        "catwalk", "objects", 'pump_room', 'aircraft_carrier_object', 'furnace_room', 'manual_labor', 'cargo_container_interior'
    ],
    "retail": [
        "gift_shop", "jewelry_shop", "shoe_shop", "pharmacy", "toyshop", "hat_shop", "betting_shop",
        "bookbindery", "dress_shop", "delicatessen", "gun_store", "optician", "perfume_shop", "piano_store",
        "cybercafe", 'fabric_store', 'liquor_store_outdoor', 'bookstore', 'shopping_mall_indoor', 
        'candy_store', 'department_store', 'clothing_store', 'liquor_store_indoor', 'liquor_store_outdoor', 'general_store_indoor'
    ],
    "sports": [
        "football_field", "basketball", "boxing_ring", "squash_court", "baseball_field", "bullring",
        "riding_arena", "ski_slope", "ski_jump", "handball_court", "hockey", "batters_box",
        "pitchers_mound", "baseball", "football", "soccer", 'basketball_court_indoor', 'badminton_court_outdoor', 'volleyball_court_outdoor', 'ice_skating_rink_outdoor', 
        'ice_skating_rink_indoor', 'athletic_field_outdoor', 'mini_golf_course_outdoor', 'wrestling_ring_indoor',
        'football', 'stadium_outdoor', 'tennis_court_indoor', 'basketball_court_outdoor', 'roller_skating_rink_outdoor', 'batting_cage_outdoor', 'wrestling_ring_outdoor', 
        'tennis_court_outdoor', 'football_field'
    ],
    "infrastructure": [
        "bridge", "dam", "aqueduct", "viaduct", "tollbooth", "overpass", "pipeline",
        "pumping_station", "windmill", "retaining_wall", "seawall", "spillway",
        'toll_plaza', 'foundry_outdoor', 'auto_racing_paddock', 'recycling_plant_outdoor', 'industrial_park', 'recycling_plant_indoor',
        'water_treatment_plant_outdoor', 'oil_refinery_indoor', 'chemical_plant',
        'tollgate', 'streetcar_track', 'cargo_deck', 'railroad_track', 'water_gate', 'road_outdoor', 'elevator_interior', 
        'road_cut', 'water_treatment_plant_indoor'
    ],
    "other": [
        "establishment", "misc", "questionable", "block", "east_asia", "rubble", "balustrade",
        "sauna", "sewer", "excavation", "dugout", "needleleaf", "howdah", "embrasure",
        "flying_buttress", "stage_set", "feed_bunk", "fire_trench", "archipelago", "arbor",
        "battlefield", "bulkhead", "drainage_ditch", "military_tent", "rainforest", "waterfall",
        "artificial", "art_studio", "construction_site", "earth_fissure", "ghost_town", "urban",
        "freestanding", "western", "south_asia", "zebra_crossing", "graveyard", "ghost_town",  'gathering_place',
        'flashflood', 'quicksand', 'power_plant_outdoor', 'furnace_room', 'storage_room', 'booth_indoor'
    ]
}



other = set()

def categorize_label(label):
    label = label.lower()
    matched_categories = set()
    for category, keywords in GENERALIZATION_RULES.items():
        # if any(kw in label for kw in keywords):
        if label in keywords:

            matched_categories.add(category)
    if not matched_categories:
        # print(label)
        other.add(label)
    # if len(matched_categories) > 2:
    #     return {"mixed"}
    return matched_categories

def process_labels(file_path="/home/paperspace/Documents/nika_space/main_dataset/labels.txt", output_path="/home/paperspace/Documents/nika_space/main_dataset/generalized_labels.txt"):
    generalized_lines = []
    with open(file_path, "r") as f:
        for line in f:
            parts = re.split(r'\s+', line.strip(), maxsplit=1)
            if len(parts) < 2:
                continue
            filename, raw_labels = parts
            labels = re.split(r'[;,]', raw_labels)
            categories = set()
            for lbl in labels:
                categories.update(categorize_label(lbl.strip()))
            generalized_line = f"{filename} {';'.join(sorted(categories))}"
            generalized_lines.append(generalized_line)

    with open(output_path, "w") as out_f:
        for line in generalized_lines:
            out_f.write(line + "\n")
    print(f"Generalized labels written to {output_path}")


process_labels()
print(other)
