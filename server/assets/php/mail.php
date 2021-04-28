<?
/**
* asdas
 */

function($content, $adress) mail_senden{

    $empfaenger = 'niemand@example.com';
    $betreff = "zeyecx.com ".$_POST[name]."<".$_POST["email"].">";
    $nachricht = $_POST["message"];
    mail($empfaenger, $betreff, $nachricht);
}

?>