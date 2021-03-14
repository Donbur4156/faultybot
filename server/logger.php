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
   fwrite($datei,$ip.";".$host.";".$datum.";".$uhrzeit.";".$token.";".$team."\n");
   fclose($datei);
}


/**
 *  create logger file
 */ 
function create_logger_file(){
    if (!file_exists('log.txt')) {   
        // create double !?
        touch('log.txt');
        }

}
?>