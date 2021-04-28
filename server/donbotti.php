<?

/**
 * User Info
 */
function user_info($token,$format_date,$formmat_time,$team){
    print("Token: ".$token."<br>"); 
    print("Tag: ".$format_date."<br>");
    print("Zeit: ".$formmat_time."<br>");
    print("Team: ".$team."<br>");
    echo "<br><h2> Cheaters from the team ". $team ."</h2>";
}

/**
 *  Content
 */
function content($zitate,$team){
    $blocked = true;
    for($i=2;$i < count($zitate); $i++){
            $user = $zitate[$i];
            if($user != "Zeyecx" &&  $user != "Eight_tlmes_ate"){
                if($i >= 2){
                    $c = $i - 1;
                    echo $c.": <a href='https://lichess.org/@/".$user."' target='_blank'>".$user."</a> <br>";
                }else{
                    echo $zitate[$i]."<br>";
                }            
            }else{
                if ($blocked  == false){
                        $blocked = true;
                    }
                }   
        }


        if($blocked){
            print("<div style='color: yellow'>The file was redacted</div>");
            print("<div style='color:black'>No users have been flagged</div>");
        }


        if ($team == ""){
            print("<h1><center> INVALID TOKEN</center> </h1>");
        }
    }
?>