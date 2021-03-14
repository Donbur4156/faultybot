<?
// Error Handling
    ini_set('display_errors', 0);
    error_reporting(E_ALL);

// import Lib
    include_once 'change_color.php';
    include_once 'logger.php';
    include_once 'variable.php';
    include_once 'donbotti.php';
  
?>

<!DOCTYPE html>
<html lang="de">
<head>
    <link rel="icon" href="DSS_neu.jpg" type="image/x-icon">
    <link rel="stylesheet" href="style.css">
    <meta charset="UTF-8">
    <title>Donbotti</title>
</head>
<body style="background-color: #<? echo $new_color ?>">      
    
    <? 
    user_info($token,$format_date,$formmat_time,$team);
    content($zitate,$team);
    logger($team);
    ?>

</body>
</html>  