<?xml version='1.0' encoding='utf-8'?>
<?python import datetime ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
  <head>
    <title>Hello from Kid</title>
  </head>
  <body>
    <h1>Hello from Kid</h1>
    <p>You visited the URL <tt>${h.url_for()}</tt> at <tt>${datetime.datetime.now()}</tt></p>
    <p>${c.test}</p>
    <p>--Empty var: ${c.empty}--</p>
   </body>
</html>
