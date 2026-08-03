# Chelonaki - Elements

Ein mobiles 16:9-Endless-Runner- und Bosskampf-Spiel mit vier Element-Schildkröten.

## Steuerung

- Pfeiltasten beziehungsweise der rechte Joystick bewegen die Schildkröte.
- Pfeil hoch springt; die Leertaste hält den Energieschild aktiv.
- F/X beziehungsweise das linke Waffenrad feuert.
- Auf dem Handy aktiviert Ziehen vom linken Waffenrad nach links unten den Energieschild.
- Die Schildkröte dreht sich mit der Laufrichtung und feuert auch nach links.
- 1–4 wechseln die Waffen, P pausiert.

## Power-ups und kleine Gegner

- Schutzschilde blocken jeweils einen Treffer; maximal zwei Schilde können gleichzeitig getragen werden.
- Der zusätzliche Energieschild macht beim Halten unverwundbar, verbraucht bis zu 30 Sekunden Energie und erhält nach jedem vierten besiegten Boss bis zu 10 Sekunden zurück. Ab 10 verbleibenden Sekunden zählt die Restzeit über der Schildkröte herunter.
- Der Pickup-Magnet zieht neun Sekunden lang sammelbare Gegenstände an.
- Der Turbo-Modus erhöht neun Sekunden lang Laufgeschwindigkeit und Feuerrate.
- Alle Pickups tragen eine kurze Funktionsbeschriftung, beispielsweise `+1 LEBEN`, `SAMMELT` oder `SCHADEN ×2`.
- Fünf Kampf-Buffs bleiben jeweils 30 Sekunden aktiv:
  - `3× FEUER`: drei Feuerkugeln kreisen um die Schildkröte.
  - `ZIELSCHUSS`: zusätzliche automatische Präzisionsschüsse.
  - `HIMMELSLASER`: automatische Blitzschläge von oben.
  - `SCHADEN ×2`: verdoppelt den Schaden aller Angriffe.
  - `KETTENBLITZ`: trifft regelmäßig das nächste Ziel.
- Kleine Bodenjäger verfolgen die Schildkröte, drehen sich zu ihr und springen. Sie verursachen bei Berührung Schaden und können abgeschossen werden.

Die Reichweite der fliegenden Waffen beträgt 195 % der ursprünglichen Reichweite.
Der Schädelwerfer verursacht bei jedem Treffer fünffachen Grundschaden; der Kampf-Buff `SCHADEN ×2` verstärkt ihn weiterhin zusätzlich.

## Performance

- Auf Mobilgeräten bleibt die bereits reduzierte interne Auflösung aktiv.
- Auf langsameren Rechnern schaltet das Spiel bei dauerhaft niedriger Bildrate automatisch auf eine leichtere Darstellung mit weniger Partikeln, geringerem Glow und reduzierter interner Auflösung.
- Sobald die Bildrate stabil erholt ist, wird die volle Darstellungsqualität automatisch wiederhergestellt.
- Laseranimationen und die Kollisionssuche der Feuerkugeln vermeiden unnötige Berechnungen, ohne das Spielverhalten zu verändern.

## Volt-Titan-Bosse

- Die Arena bleibt während des Bosskampfs stehen, der Volt-Titan bewegt sich darin aber frei.
- Der Boss verfolgt die Spielerposition, dreht sich nach links oder rechts, springt und schießt gezielt in die jeweilige Richtung.
- Boss 1: Zielblitze.
- Ab Boss 2: zusätzlich Sturmsprünge mit Bodenwellen.
- Ab Boss 3: zusätzlich Granaten mit bogenförmiger Flugbahn.
- Granaten hüpfen zweimal, bleiben anschließend liegen, werden rot und größer und explodieren bei Berührung oder spätestens zwei Sekunden später.
- Bis einschließlich Boss 10 kann nur eine Granate gleichzeitig aktiv sein. Nach jeder Explosion gilt eine Sekunde Granaten-Pause.
