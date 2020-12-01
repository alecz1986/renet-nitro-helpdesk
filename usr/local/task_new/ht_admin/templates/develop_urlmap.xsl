<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class="tsimple">
      <tbody>
        <xsl:for-each select="/R/tables/labels">
          <tr><th colspan="2"><div>Метка: <xsl:value-of select="label"/></div></th></tr>
          <xsl:choose>
            <xsl:when test="count(urlmap/*)!=0">
              <tr><th><div>Путь</div></th><th><div>Модуль</div></th></tr>
              <xsl:for-each select="urlmap/*">
                <tr>
                  <td>
                    <div>
                      <xsl:element name="a">
                        <xsl:attribute name="href">
                          <xsl:text>/private/develop/urlmap_edit?url_label=</xsl:text><xsl:value-of select="../../label"/>
                          <xsl:text>&amp;url_path=</xsl:text><xsl:value-of select="path"/>
                        </xsl:attribute>
                        <xsl:value-of select="path"/>
                      </xsl:element>
                    </div>
                  </td>
                  <td>
                    <div>
                      <xsl:element name="a">
                        <xsl:attribute name="href">
                          <xsl:text>/private/develop/urlmap_edit?url_label=</xsl:text><xsl:value-of select="../../label"/>
                          <xsl:text>&amp;url_path=</xsl:text><xsl:value-of select="path"/>
                        </xsl:attribute>
                        <xsl:value-of select="resporator"/>
                      </xsl:element>
                    </div>
                  </td>
                </tr>
              </xsl:for-each>
            </xsl:when>
            <xsl:otherwise>
              <tr><td colspan="2"><div>Нет записей</div></td></tr>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:for-each>
      </tbody>
    </table>
  </xsl:template>
</xsl:stylesheet>
