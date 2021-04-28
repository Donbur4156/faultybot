<?
/**
* asdas
 */

function mail_senden($content, $adress){

    $empfaenger = 'niemand@example.com';
    $betreff = "zeyecx.com ".$_POST[name]."<".$_POST["email"].">";
    $nachricht = $_POST["message"];
    mail($empfaenger, $betreff, $nachricht);
}

?>