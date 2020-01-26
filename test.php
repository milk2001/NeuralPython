<!DOCTYPE html>
    <html lang="it">

    <head>
        <meta charset="utf-8">
        <title>cat or dog?</title>
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">  <!--importazione css Bootstrap-->
        <!-- regole di stile-->
        <style>
            .float-right{
              padding: 15px;
            }
            .titolo{

              padding-top: 30px;
            }
            .bottone{
              margin-top: 20px;
            }
        </style>
    </head>

    <body>

        <div class="container h-100">
            <div class="row h-30 justify-content-center align-items-center">
                <h1 class="titolo" >cat or dog?</h1>
            </div>
            <div class="row h-100 justify-content-center align-items-center">
                <form name="img" action="" method="POST" enctype="multipart/form-data">
                    <input name="foto" class="form-control" type="file" />
                    <small class="form-text text-muted">Supporta jpeg, png, jpg. MAX 10Mb.</small>
                    <input type="submit" class="btn btn-primary bottone" />
                </form>
</div>
<div class="row h-100 justify-content-center align-items-center">



  <?php

  if (!empty($_FILES['foto']) && is_uploaded_file($_FILES["foto"]["tmp_name"])) {
    $errors= false;
    $tmpfile = $_FILES["foto"]["tmp_name"];
      $file_size = $_FILES['foto']['size'];
      $filename = basename($_FILES['foto']['name']);
      $tmp = explode('.', $_FILES['foto']['name']);
      $file_ext =strtolower(end($tmp));
      $extensions= array("jpeg","jpg","png");
      if (in_array($file_ext, $extensions)=== false) {
        $errors=true;
          echo"<p> Estensione file foto non valida, riprovare.</p>";
      }

      if ($file_size > 10485760) {
          $errors=true;
          echo "<p> Il file deve essre al massimo di 10 MB.</p>";
      }


      $curlFile = curl_file_create($tmpfile);
      $post = array('image'=> $curlFile );
      $ch = curl_init();
      curl_setopt($ch, CURLOPT_URL,"http://localhost:5000");
      curl_setopt($ch, CURLOPT_POST,1);
      curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
      curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
      $result=curl_exec($ch);
      curl_close ($ch);
      $json = json_decode($result);
      if ($errors==false) {
          move_uploaded_file($_FILES["foto"]["tmp_name"], "./upload." . $file_ext);
      //  echo "Success";
      } else {
          $errors=true;
          echo "<p> Errore caricamento file.</p>";
      }
      echo("Animale: ");
      echo($json->{"animal"});
      echo("<br>Gatto al ");
      echo($json->{"cat"});
      echo("%");
      echo("<br>Cane al ");
      echo($json->{"dog"});
      echo("%");
      echo("<img src=\"");
      echo("/upload.".$file_ext);
      echo("\">");
}?>
</div>
</div>
<footer class="py-4 text-white-50">
<div class="container text-center">
Picasso, 2019
</div>
</footer>
<!-- script per il corretto funzionamento di Bootsrap-->
<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
    </body>

    </html>
