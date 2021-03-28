<?
 
/**
 * Logger
 */
function logger($team){
   create_logger_file();
   $datei = fopen("log.csv", "a+");
   $ip = $_SERVER["REMOTE_ADDR"];  
   $host = gethostbyaddr($ip);
   $datum = date("d.m.Y",time());
   $uhrzeit = date("H:i",time());
   $token = $_GET['token'];

   

   if($token == ""){
      $token = "Invalid Token";
      $team = "Invalid Team";
      };


   $data = array($ip,$host,$datum,$uhrzeit,$token,strval($team));
   fputcsv($datei, explode(";",$data));
   fclose($datei);
}


/**
 *  create logger file
 */ 
function create_logger_file(){
    if (!file_exists('log.csv')) {   
      touch('log.csv');
      $datei = fopen("log.csv", "a+");
      $data = array("IP","Host","Datum","Uhrzeit","Token","Team");
      fputcsv($datei, explode(";",$data));
      fclose($datei);
        }

}
?>