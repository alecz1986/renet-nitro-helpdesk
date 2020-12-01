<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <br/>
    <form name="form.se" method="POST">
      <xsl:attribute name="enctype"><xsl:choose>
          <xsl:when test="/R/form/@multipart"><xsl:text>multipart/form-data</xsl:text></xsl:when>
          <xsl:otherwise><xsl:text>application/x-www-form-urlencoded</xsl:text></xsl:otherwise>
      </xsl:choose></xsl:attribute>
      <xsl:attribute name="action"><xsl:value-of select="/R/page/path_info"/></xsl:attribute>
      <xsl:for-each select="/R/form/*">
        <xsl:if test="ftype[text()='hidden']">
          <div>
            <xsl:element name="input">
              <xsl:attribute name="type">hidden</xsl:attribute>
              <xsl:attribute name="name"><xsl:value-of select="name"/></xsl:attribute>
              <xsl:attribute name="id"><xsl:text>se.</xsl:text><xsl:value-of select="name"/></xsl:attribute>
              <xsl:attribute name="value"><xsl:value-of select="value"/></xsl:attribute>
            </xsl:element>
          </div>
        </xsl:if>
      </xsl:for-each>
      <table class="tsimple">
        <xsl:choose>
          <xsl:when test="/R/form/action/value[text()='new']">
            <thead>
              <tr><th colspan="2"><div id="st._head_" css:color="green">Создание новой записи</div></th></tr>
            </thead>
          </xsl:when>
          <xsl:when test="/R/form/action/value[text()='edit']">
            <thead>
              <tr><th colspan="2"><div id="st._head_" css:color="red">Режим редактирования</div></th></tr>
            </thead>
          </xsl:when>
        </xsl:choose>
        <tbody>
          <xsl:for-each select="/R/form/*">
            <xsl:if test="ftype[text()!='hidden']">
            <tr>
              <th>
                <xsl:element name="div">
                  <xsl:attribute name="id"><xsl:text>st.</xsl:text><xsl:value-of select="name"/></xsl:attribute>
                  <xsl:value-of select="label"/>
                </xsl:element>
              </th>
              <td><div>
              <xsl:choose>
                <xsl:when test="ftype[text()='select']">
                  <xsl:element name="select">
                    <xsl:attribute name="name"><xsl:value-of select="name"/></xsl:attribute>
                    <xsl:attribute name="id"><xsl:text>se.</xsl:text><xsl:value-of select="name"/></xsl:attribute>
                    <xsl:for-each select="options/*">
                      <xsl:element name="option">
                        <xsl:attribute name="value"><xsl:value-of select="value"/></xsl:attribute>
                        <xsl:if test="../../value[1]=value[1]"><xsl:attribute name="selected"></xsl:attribute></xsl:if>
                        <xsl:value-of select="text()"/>
                      </xsl:element>
                    </xsl:for-each>
                  </xsl:element>
                </xsl:when>
                <xsl:when test="ftype[text()='textarea']">
                  <xsl:element name="textarea">
                    <xsl:attribute name="name"><xsl:value-of select="name"/></xsl:attribute>
                    <xsl:choose>
                      <xsl:when test="name[text()='text']">
                        <xsl:attribute name="cols">100</xsl:attribute>
                        <xsl:attribute name="rows">40</xsl:attribute>
                      </xsl:when>
                      <xsl:otherwise>
                        <xsl:attribute name="cols">100</xsl:attribute>
                        <xsl:attribute name="rows">5</xsl:attribute>
                      </xsl:otherwise>
                    </xsl:choose>
                    <xsl:attribute name="id"><xsl:text>se.</xsl:text><xsl:value-of select="name"/></xsl:attribute>
                    <xsl:value-of select="value"/>
                  </xsl:element>
                </xsl:when>
                <xsl:when test="ftype[text()='date']">
                  <xsl:element name="input">
                    <xsl:attribute name="type">text</xsl:attribute>
                    <xsl:attribute name="name"><xsl:value-of select="name"/></xsl:attribute>
                    <xsl:attribute name="id"><xsl:text>se.</xsl:text><xsl:value-of select="name"/></xsl:attribute>
                    <xsl:attribute name="value"><xsl:value-of select="value"/></xsl:attribute>
                  </xsl:element>
                  <xsl:element name="input">
                    <xsl:attribute name="width">20</xsl:attribute>
                    <xsl:attribute name="type">submit</xsl:attribute>
                    <xsl:attribute name="value">#</xsl:attribute>
                    <xsl:attribute name="id">trigger<xsl:value-of select="name"/></xsl:attribute>
                  </xsl:element>
                    <script type="text/javascript">
                      <![CDATA[
                               Calendar.setup({
                               inputField     :    "]]><xsl:text>se.</xsl:text><xsl:value-of select="name"/><![CDATA[",
                                ifFormat       :    "%Y-%m-%d",
                                button         :    "]]>trigger<xsl:value-of select="name"/><![CDATA[",
                                align          :    "Tl",
                                singleClick    :    true
                                });]]>
                         </script>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:element name="input">
                    <xsl:attribute name="type"><xsl:value-of select="ftype"/></xsl:attribute>
                    <xsl:attribute name="name"><xsl:value-of select="name"/></xsl:attribute>
                    <xsl:attribute name="id"><xsl:text>se.</xsl:text><xsl:value-of select="name"/></xsl:attribute>
                    <xsl:attribute name="value"><xsl:value-of select="value"/></xsl:attribute>
                  </xsl:element>
                </xsl:otherwise>
              </xsl:choose>
              </div></td>
            </tr>
            </xsl:if>
          </xsl:for-each>
          <tr><td colspan='2'>
            <xsl:if test="/R/data/rich">
              <script type="text/javascript">
                <![CDATA[
                function unescapeHTML(html) {
                  var htmlNode = document.createElement("DIV");
                  htmlNode.innerHTML = html;
                  if(htmlNode.innerText)
                    return htmlNode.innerText; // IE
                  return htmlNode.textContent; // FF
                }
                var editor1 = new EDITOR();
                editor1.create(unescapeHTML(']]><xsl:value-of select='/R/data/@text'/><![CDATA['));
                ]]>
              </script>
            </xsl:if>
          </td></tr>
          <tr>
            <td colspan="2"><div>
                <xsl:choose>
                  <xsl:when test='/R/data/rich'>
                    <input type="submit"  value="  OK  " onClick="rtoStore()"/>
                  </xsl:when>
                  <xsl:otherwise>
                    <input type="submit" id="se.submit" value="  OK  "/>
                  </xsl:otherwise>
                </xsl:choose>
            </div></td>
          </tr>
        </tbody>
      </table>
    </form>
  </xsl:template>
</xsl:stylesheet>
