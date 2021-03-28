<?
		if(isset($_GET['token']) && $_GET['r'] != "0"){
			$url = "https://www.zeyecx.com/p/Donbotti/index.php?token=".$_GET['token']."&r=0#donbotti";
			header("Location: ".$url);
		}
?>

<!DOCTYPE HTML>
<html>
	<head>
	


		<title>Zeyecx</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="assets/css/main.css" />
		<link rel="shortcut icon"  href="DSS_neu.jpg">
		<noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>	
	</head>
	<?
	if($mobile){
		print("<body class='is-preload' style='margin-top: 0px'>");
	}else{
		print("<body class='is-preload'>");
	}
	?>	
	

		<!-- Wrapper -->
			<div id="wrapper">
				<!-- Header -->
					<header id="header">
						<div class="logo">
							<span class="icon fa-gem"></span>
						</div>
						<div class="content">
							<div class="inner">
								<h1>Donbotti</h1>
								<p>Find all cheaters in your Lichess team.</p>
							</div>
						</div>
						<nav>
							<ul>
								<li><a href="https://www.zeyecx.com">Zeyecx</a></li>
								<li><a href="#id">Token</a></li>
								<li><a href="#author">Author</a></li>
								<li><a href="https://github.com/jplight/faultybot" target="_blank">Code</a></li>
								<li><a href="https://github.com/jplight/faultybot/archive/refs/heads/main.zip" target="_blank">Download</a></li>
								<?
									if(isset($_GET['token']) && $_GET['token'] != ""){
										print("<li><a href='#donbotti'>Übersicht</a></li>");
									}

								?>
							</ul>
						</nav>
					</header>

				<!-- Main -->
					<div id="main">
						<!-- ID -->
							<article id="id">
								<h2 class="major">Token</h2>
								<span class="image main"><img src="images/pic02.jpg" alt="" /></span>
								<form action="https://www.zeyecx.com/p/Donbotti/index.php#donbotti" id="token">				
								<label for="token">Bitte geben Sie einen Token ein:</label>  
								<input type="text" name="token" id="token" maxlength="8" minlength="8">
								<button type="reset">Eingaben zurücksetzen</button>
								<button type="submit">Eingaben absenden</button>
							</form>
							</article>

							<!-- Donbur -->
							<article id="author">
								<h2 class="major">Author</h2>
								<span class="image main"><img src="images/pic02.jpg" alt="" /></span>
								<h2><center> Donbur :) </center> </h2>
							</article>

						<!-- Donbotti -->
							<article id="donbotti">
								<h2 class="major">Donbotti</h2>
								<span class="image main"><img src="images/pic03.jpg" alt="" /></span>
								<p>
								<? 
									include __DIR__.'/change_color.php';
									include __DIR__.'/logger.php';
									include __DIR__.'/variable.php';
									include __DIR__.'/donbotti.php';
									//user_info($token,$format_date,$formmat_time,$team);
									print("<h3> Cheater aus dem Team:".$team."</h3><br>");
									logger($team);
									content($zitate,$team);
								?>
								</p>
							</article>
					</div>
			</div>

		<!-- BG -->
			<div id="bg"></div>


	<!-- Scripts -->
	<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/browser.min.js"></script>
			<script src="assets/js/breakpoints.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>
	</body>
</html>