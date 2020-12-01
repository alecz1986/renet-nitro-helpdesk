<xsl:stylesheet version="1.0" xmlns="http://www.w3.org/1999/xhtml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:output method="xml"/>
  <xsl:template match="/">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <title id="page.title"><xsl:value-of select="/R/page/title"/></title>
    <xsl:for-each select="/R/external/*">
      <xsl:call-template name="external"/>
    </xsl:for-each>
    <link rel="STYLESHEET"   href="/css/style_admin.css"/>
    <script type="text/javascript" src="/js/calendar.js"></script>
    <script type="text/javascript" src="/js/calendar-ru.js"></script>
    <script type="text/javascript" src="/js/calendar-setup.js"></script>
    <script type="text/javascript" src="/js/menu.js"></script>
    <script type="text/javascript" src="/js/onL.js"></script>
    <script type="text/javascript" src="/js/get_params.js"></script>
    <script type="text/javascript" src="/js/jquery-1.2.6.js"></script>
    <script type="text/javascript" src="/js/changebackground.js"></script>

    <script src="/timeplot/api/1.0/timeplot-api.js?local" type="text/javascript"></script>
	<script type="text/javascript">
	        var timeplot;
      		var resizeTimerID = null;
		function onResize() {
		      if (resizeTimerID == null) {
		      resizeTimerID = window.setTimeout(function() {
		      resizeTimerID = null;
		      timeplot.repaint();
		      }, 100);
		 }
		}
		 var color = new Array('red', '#000080', '#006400', '#B22222', 'black','#FF1493', '#CC00CC',  '#8B0A50','#660066', '#0033CC', '#666600', '#666666', 'green', 'blue', '#000000', '#B22222', '#CC0099', '#663300', '#6633CC', '#663366', '#00FFFF', '#000080', '#006400', '#B22222', 'black',  '#8B0A50','#660066', '#0033CC')
		var all = '';

</script>
  </head>
  <body css:font-size="0.8em" css:font-family="Arial,Verdana,Helvetica,sans-serif" css:background-color="white" css:margin="0px 0px 0px 0px" onload="onLo();" onresize="onResize();">
    <table class="thead" id="page.head">
      <tbody>
        <tr>
          <td css:width="35%">
            <xsl:if test="/R/page/search">
              <xsl:element name="form">
                <xsl:attribute name="name">search_form</xsl:attribute>
                <xsl:attribute name="method">post</xsl:attribute>
                <xsl:attribute name="action"><xsl:value-of select="/R/path/uri"/></xsl:attribute>
                <div>
                  <input type="text" name="search_key"/>
                  <input type="submit" value="OK"/>
                </div>
              </xsl:element>
            </xsl:if>
          </td>
          <td css:width="30%" css:text-align="center" css:font-weight="bold"><div><xsl:value-of select="/R/product/fullname"/></div></td>
          <td css:width="35%" css:text-align="right" css:font-size="8pt">
            <div>
              <xsl:if test="/R/user/*">
                <a name="url_back" href="javascript:history.back()">Back</a>
                <xsl:text> | </xsl:text>
                <xsl:element name="a">
                  <xsl:attribute name="id">upper.link-to-up</xsl:attribute>
                  <xsl:attribute name="href"><xsl:value-of select="/R/page/path_up"/></xsl:attribute>
                  <xsl:text>Up</xsl:text>
                </xsl:element>
                <xsl:text> | </xsl:text>
                <xsl:element name="a">
                  <xsl:attribute name="id">upper.link-menu</xsl:attribute>
                  <xsl:attribute name="href"><xsl:value-of select="/R/page/path_menu"/></xsl:attribute>
                  <xsl:text>Menu</xsl:text>
                </xsl:element>
                <xsl:text> | </xsl:text>
                <xsl:element name="a">
                  <xsl:attribute name="id">upper.change-a-user-secret</xsl:attribute>
                  <xsl:attribute name="href"><xsl:value-of select="/R/product/url_chgsecret"/></xsl:attribute>
                  <xsl:text>Secret</xsl:text>
                </xsl:element>
                <xsl:text> | </xsl:text>
                <xsl:element name="a">
                  <xsl:attribute name="id">upper.logout</xsl:attribute>
                  <xsl:attribute name="href"><xsl:value-of select="/R/product/url_logout"/></xsl:attribute>
                  <xsl:text>Logout</xsl:text>
                </xsl:element>
              </xsl:if>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <div css:padding-left="15%" css:padding-right="15%" id="page.body">
      <hr css:width="100%" css:text-align="center"/>
      <br/>
      <xsl:if test="/R/page/title">
        <h4 css:color="#102010" css:text-decoration="underline"><xsl:value-of select="/R/page/title"/></h4>
      </xsl:if>
      <xi:bind name="form"/>
      <br/>
      <xi:bind name="body"/>
      <xi:bind name="menu"/>
      <br/>
      <xsl:if test="/R/errors/error | /R/results/result">
        <table class="menu">
          <tbody>
            <xsl:for-each select="/R/errors/error">
              <tr><td><div css:color="red"><xsl:value-of select="."/></div></td></tr>
            </xsl:for-each>
            <xsl:for-each select="/R/results/result">
              <tr><td><div css:color="blue"><xsl:value-of select="."/></div></td></tr>
            </xsl:for-each>
          </tbody>
        </table>
        <br/>
      </xsl:if>
      <xi:bind name="other"/>
      <hr css:width="100%" css:text-align="center"/>
    </div>
    <table class="thead" id="page.tail">
      <tbody>
        <tr css:vertical-align="top">
          <td css:width="35%" css:text-align="left">
            <div css:margin-left="20px">Copyright &#169; <a id="bottom.copyright" href="http://www.renet.ru/">Renet COM</a></div>
          </td>
          <td css:width="30%" css:text-align="center" css:color="#333333"><div id="page.msg"></div></td>
          <td css:width="35%" css:text-align="right" css:color="#202080">
            <xsl:if test="not(/R/user/*)"><div css:color="blue">UNAUTHORIZED</div></xsl:if>
            <xsl:if test="/R/user/*"><div>
                <xsl:element name="a">
                  <xsl:attribute name="href"><xsl:value-of select="/R/user/viewoper"/></xsl:attribute>
                  <xsl:value-of select="/R/user/login"/>
                </xsl:element>
                <xsl:text> :: </xsl:text>
                <xsl:element name="a">
                  <xsl:attribute name="href"><xsl:value-of select="/R/user/viewgroup"/></xsl:attribute>
                  <xsl:value-of select="/R/user/group"/>
                </xsl:element>
            </div></xsl:if>
          </td>
        </tr>
      </tbody>
    </table>
  </body>
</html>
  </xsl:template>
  <xsl:template name="external">
    <xsl:choose>
      <xsl:when test="name()='js'">
        <xsl:element name="script">
          <xsl:attribute name="type">text/javascript</xsl:attribute>
          <xsl:attribute name="src"><xsl:value-of select="./text()"/></xsl:attribute>
        </xsl:element>
      </xsl:when>
      <xsl:when test="name()='css'">
        <xsl:element name="link">
          <xsl:attribute name="rel">stylesheet</xsl:attribute>
          <xsl:attribute name="type">text/css</xsl:attribute>
          <xsl:attribute name="href"><xsl:value-of select="./text()"/></xsl:attribute>
        </xsl:element>
      </xsl:when>
      <xsl:otherwise>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>
