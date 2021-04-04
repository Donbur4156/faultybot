<?
 
/**
 * Logger
 */
function logger($team){
   create_logger_file();
   $datei = fopen("log.txt", "a+");
   $ip = $_SERVER["REMOTE_ADDR"];  
   $host = gethostbyaddr($ip);
   $datum = date("d.m.Y",time());
   $uhrzeit = date("H:i",time());
   $token = $_GET['token'];

   

   if($token == ""){
      $token = "Invalid Token";
      $team = "Invalid Team";
      };


   $data = $ip.";".$host.";".$datum.";".$uhrzeit.";".$token.";".strval($team)."\n";
   fwrite($datei, $data);
   fclose($datei);
}


/**
 *  create logger file
 */ 
function create_logger_file(){
    if (!file_exists('log.txt')) {   
      // touch('log.txt');
      $datei = fopen("log.txt", "a+");
      $data =  "IP; Host; Datum; Uhrzeit; Token; Team \n"   ;
      fwrite($datei, $data);
      fclose($datei);
        }
}
?>