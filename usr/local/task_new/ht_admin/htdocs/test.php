<?php
if(isset($_GET['id']) && is_numeric($_GET['id'])){
    @system("/usr/local/bin/php connect.php ".(int)($_GET['id']));
}
?>