Area 1 result is ready — Visual style direction.

Please log this as the visual direction for the main project before making repo decisions.

Chosen direction:
2D illustrated storybook academic fantasy with a parchment academic UI, cosy medieval cottage hub, paper-doll character layering, and darker cave/dungeon screens for the academic work quests.

Main visual identity:
Academic adventurer / cosy fantasy / medieval cottage / scholar quest log / paper-doll wardrobe.

Important visual decisions:
- The character should stay in the soft illustrated anime/storybook style from the Academic Adventurer references.
- The house exterior should use the cosy illustrated cottage direction.
- The game should feel like a living illustrated journal rather than a normal moving game map.
- The pixel-game screenshot is useful only for layout inspiration, not for the final art style.
- Screens should be static and layered to avoid lag.
- UI should use parchment panels, brown ink borders, old paper labels, wooden tags, wax seals, brass details, and journal/quest-log styling.
- The house, wardrobe, edit room, mood board, cave, and academic quest screens should all share the same parchment/storybook visual system.

Colour palette:
Parchment cream, ink brown, weathered wood, soft gold, forest green, dusty rose, burgundy/plum, dark scholar navy, muted teal, and moss green.

Texture/pattern direction:
Parchment grain, worn leather, lace, plaid, old wood, stone, botanical embroidery, fabric swatches, scroll edges, hand-drawn borders.

Character notes:
Keep long blonde hair, gentle academic-adventurer expression, boots, satchel, layered necklaces, botanical tattoos, soft fantasy clothing, and paper-doll outfit layering. The base character should eventually be prepared for transparent clothing overlays.

House/interior notes:
The interior should become a cosy scholar-adventurer cottage room with wardrobe, mirror, desk, bookshelves, edit-room/mood-board access, chest, rug slot, wallpaper slot, and cave/work entrance.

Edit room notes:
The edit room should include a clickable mood board wall. The mood board should later hold pinned notes, essay sections, quotes, keywords, command words, visual inspo, colour/pattern swatches, and “return later” flags.

Cave/dungeon notes:
The cave should be darker but not horror. It should feel like an academic quest dungeon with static monster screens, glowing crystals, parchment UI, stone textures, scrolls, loot, locked gates, and a boss-room writing stage.

Version 0.1 visual priorities:
- outside house static screen
- character layer on exterior
- click-to-enter interaction
- inside house hub
- clickable mirror placeholder
- clickable wardrobe placeholder
- clickable edit room/mood board placeholder
- clickable cave/work entrance placeholder
- fixed furniture slot placeholders
- parchment-style UI
- static layered screens, no open world movement

Future visual ideas:
Character poses, outfit layers, seasonal house variants, furniture sets, editable wallpaper/carpet patterns, mood board skins, cave zones, monster cards, reward animations, and parchment progress reports.

Avoid:
Pixel-art final style, real-photo backgrounds without illustration treatment, modern flat UI, neon mobile-game reward effects, free furniture dragging too early, heavy animation, too many palettes, and inconsistent generated assets.

Request for repo/master chat:
Please fold Area 1 into the master project plan and use it to guide Version 0.1 visual shell decisions. Do not implement advanced customisation yet. The next repo decision should be whether the current messy repo can support this static layered visual shell or whether we should start fresh.

AREA 2 — BASE CHARACTER DESIGN RESULT

This is the result from the Area 2 branch. Please log this as the current character design direction for the main game project. Do not restructure the repo from this alone. Use it to guide character assets, screen planning, and future implementation.

CORE CHARACTER DIRECTION

The main character direction is working and should be kept.

She is a soft illustrated pixel-fantasy heroine with long warm blonde hair, a gentle storybook face, feminine proportions, and a medieval/renaissance explorer identity. The current images should be treated as design inspiration and production direction, not final locked game-ready assets yet.

The key decision is that the character should have two main visual modes:

1. LIGHT / HOME MODE

The lighter pink/soft version is for:
- outside house
- inside house hub
- edit room
- mood board
- mirror
- wardrobe
- home planning screens
- calmer task areas
- reward/level-up moments

This version should feel safe, soft, pretty, home-based, and motivating.

2. DARK / CAVE MODE

The darker explorer version is for:
- cave system
- dungeon/quest screens
- academic work combat
- monster screens
- boss fight stages
- source mine
- quote bank work
- draft tunnel
- harder work stages

This version should feel more prepared, practical, quest-ready, and serious.

IMPORTANT SYSTEM RULE

The game should support location-based character outfit states.

Example:
home_area_character = light outfit
edit_room_character = light outfit
wardrobe_character = neutral or light outfit
cave_area_character = dark explorer outfit
boss_area_character = dark explorer outfit

The character is not changing identity between these modes. The same base character remains consistent across both:
- same face
- same hair
- same body proportions
- same general art style
- same character identity
- same optional tattoos if kept active

IMAGE USE NOTES

Image 1:
This is the strongest structural reference. Use it as the base character reference because it includes front, 3/4 front, side, back, walking, face close-up, tattoo close-up, and neutral base clothing. It is the best reference for body proportions, face, hair, base outfit, and future layering.

Light/pink outfit images:
These should be treated as the home-area character direction. They are not just optional extras. They define the character’s safe/home/edit-room/wardrobe mood.

Dark outfit images:
These should be treated as the cave/work-combat character direction. They are not the everyday default for every screen. They belong to the academic quest system, monsters, boss fights, and dungeon work areas.

Book/reading pose:
This is important for the academic work system. It can exist in either light or dark mode depending on whether the screen is a home study area or a cave/source/quest area.

Cleaning pose:
This is useful later for house tasks, edit-room upkeep, chore tasks, room improvement, or visual feedback when maintaining the house.

Victory pose:
This is useful later for completing tasks, unlocking rewards, levelling up, and finishing quest stages.

Mirror/wardrobe pose:
The softer pose where she is playing with her hair is useful later for the wardrobe, mirror, appearance screen, or outfit preview.

BASE ASSET STRUCTURE

The character should eventually be built as layers, not as one permanently baked image.

Preferred layer logic:
- base body
- hair
- base tank top and shorts or simple neutral underlayer
- arm tattoo overlay
- thigh tattoo overlay
- top clothing layer
- bottom clothing layer
- dress / overskirt layer
- boots layer
- bag / accessory layer
- prop layer
- expression / pose variant

Do not permanently bake the following into the universal base if avoidable:
- satchel
- necklaces
- boots
- belts
- tattoos
- bags
- props
- books
- broom
- cleaning tools
- outer skirt panels

These should be treated as separate or semi-separate assets where possible so wardrobe, unlocks, and screen-specific poses remain manageable later.

VERSION 0.1 REQUIREMENT

For Version 0.1, we only need one clean static character layer. It does not need full animation or full clothing layering yet.

The best Version 0.1 character asset would be:
- clean front-facing or slight 3/4 standing character
- transparent background
- light/home mode outfit first if starting with the house hub
- dark/cave mode saved as the next required version
- consistent scale so she can be placed over house and cave backgrounds

FUTURE REQUIREMENTS

Later, the game should support:
- light home outfit state
- dark cave outfit state
- wardrobe outfit unlocks
- mirror/appearance screen
- pose changes by room or quest area
- study/book pose
- victory pose
- cleaning/house task pose
- cave/boss pose
- transparent background exports
- consistent sizing across all character files

FINAL AREA 2 SUMMARY

The character should have two main outfit modes: the lighter version for home, edit room, wardrobe, mirror, and calm planning areas, and the darker explorer version for the cave, monsters, academic quest stages, and boss fight. Both modes must keep the same base face, hair, body, and soft illustrated pixel-fantasy style. Image 1 is the structural base reference. The current priority is making one clean Version 0.1 static character layer before building full wardrobe or pose systems.
