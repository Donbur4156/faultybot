<?
/**
 * Token von dem Donbotti
 */
  $token = $_GET['token']; 
  
  /**
   * Path zur *.flag Datei
   */
  $flag_file = dirname(__FILE__)."/flag/".$token.".flag";
  
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
   * Lese Datei als Array ein
   */
  $zitate = file($flag_file);

  /**
   * Liest Teamname aus Datei ein. 
   */
  $team = $zitate[1];

  /**
   * gibt die neue Farbe an
   */
  $new_color = random_color();
?>