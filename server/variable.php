<?

/**
 * Token from the Donbotti
 */
$token = $_GET['token'];

/**
 * Path to the *.flag file
 */
$flag_file = dirname(__FILE__) . "/flag/" . $token . ".flag";

/**
 * Ermittle wann die Datei zuletzt benutzt wurde
 */
$date = filectime($flag_file);

/**
 * Formate CTime
 */
$format_date = date(' m.d.y', $date);
$formmat_time = date('H:i:s', $date);


/**
 * Check blocked User (Beispiel: 8x8)
 */
$blocked = false;

/**
 * Read file as array
 */
$zitate = file($flag_file);

/**
 * Reads team name from file. 
 */
$team = $zitate[1];
