<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <!--      <div class='left-column' css:padding-top="5px">-->
        <xi:bind name="search"/>
        <xsl:call-template name="k_object">
          <xsl:with-param name="k_iter" select="/R/page/category"/>
        </xsl:call-template>
        <br/>
        <xi:bind name="banners-left"/>
        <!--  </div>-->
  </xsl:template>
  <xsl:template name="k_object">
    <xsl:param name="k_iter" select="."/>
    <xsl:param name="name" select="./@name"/>
    <xsl:if test="($k_iter)/*">
      <ul class="menu">
        <xsl:for-each select="($k_iter)/*">
          <xsl:choose>
            <xsl:when test="/R/page/@opt = 'yes'">
              <xsl:if test="@opt=/R/page/@opt">
                <li>
                  <xsl:element name='a'>
                    <xsl:attribute name="css:white-space"><xsl:text>pre-wrap</xsl:text></xsl:attribute>
                    <xsl:attribute name='href'>/<xsl:value-of select='@template'/>?category_id=<xsl:value-of select='@id'/></xsl:attribute>
                    <xsl:if test="@id = '321758'">
                      <xsl:attribute name='target'>_blank</xsl:attribute>
                      <xsl:attribute name='css:background-color'>#00CC33</xsl:attribute>
                      <xsl:attribute name='css:background-image'>url("http://peshca.ru/img/menu_dot_green.gif")</xsl:attribute>
                    </xsl:if>
                    <xsl:if test="@action = 'true'">
                      <xsl:attribute name='class'>click</xsl:attribute>
                    </xsl:if>
                    <xsl:if test="@new = 'ye'">
                      <xsl:attribute name='css:text-decoration'>underline</xsl:attribute>
                      <xsl:attribute name='css:color'>#C50069</xsl:attribute>
                    </xsl:if>
                    <xsl:choose>
                      <xsl:when test="@action = 'true' and @root!='0'">
                        <xsl:text> - </xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:if test="@plus='1' and @root!='0'">
                          <xsl:text> + </xsl:text>
                        </xsl:if>
                        <xsl:if test="@plus='0' and @root!='0'">
                          <xsl:text> - </xsl:text>
                       </xsl:if>
                    </xsl:otherwise>
                  </xsl:choose>
                  <xsl:value-of select="@name"/>
                  </xsl:element>
                  <xsl:call-template name="k_object"/>
                </li>
              </xsl:if>
            </xsl:when>
            <xsl:when test="/R/page/@desk = 'yes'">
              <xsl:if test="@desk=/R/page/@desk">
                <li>
                  <xsl:element name='a'>
                    <xsl:attribute name="css:white-space"><xsl:text>pre-wrap</xsl:text></xsl:attribute>
                    <xsl:attribute name='href'>/<xsl:value-of select='@template'/>?category_id=<xsl:value-of select='@id'/></xsl:attribute>
                    <xsl:if test="@id = '321758'">
                      <xsl:attribute name='target'>_blank</xsl:attribute>
                      <xsl:attribute name='css:background-color'>#00CC33</xsl:attribute>
                      <xsl:attribute name='css:background-image'>url("http://peshca.ru/img/menu_dot_green.gif")</xsl:attribute>
                    </xsl:if>
                    <xsl:if test="@action = 'true'">
                      <xsl:attribute name='class'>click</xsl:attribute>
                    </xsl:if>
                    <xsl:if test="@new = 'ye'">
                      <xsl:attribute name='css:text-decoration'>underline</xsl:attribute>
                      <xsl:attribute name='css:color'>#C50069</xsl:attribute>
                    </xsl:if>
                    <xsl:choose>
                      <xsl:when test="@action = 'true' and @root!='0'">
                        <xsl:text> - </xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:if test="@plus='1' and @root!='0'">
                          <xsl:text> + </xsl:text>
                        </xsl:if>
                        <xsl:if test="@plus='0' and @root!='0'">
                          <xsl:text> - </xsl:text>
                       </xsl:if>
                    </xsl:otherwise>
                  </xsl:choose>
                  <xsl:value-of select="@name"/>
                  </xsl:element>
                  <xsl:call-template name="k_object"/>
                </li>
              </xsl:if>
            </xsl:when>
            <xsl:otherwise>
              <xsl:if test="@opt=/R/page/@opt">
                <li>
                  <xsl:element name='a'>
                    <xsl:attribute name="css:white-space"><xsl:text>pre-wrap</xsl:text></xsl:attribute>
                    <xsl:attribute name='href'>/<xsl:value-of select='@template'/>?category_id=<xsl:value-of select='@id'/></xsl:attribute>
                    <xsl:if test="@id = '321758'">
                      <xsl:attribute name='target'>_blank</xsl:attribute>
                      <xsl:attribute name='css:background-color'>#00CC33</xsl:attribute>
                      <xsl:attribute name='css:background-image'>url("http://peshca.ru/img/menu_dot_green.gif")</xsl:attribute>
                    </xsl:if>
                    <xsl:if test="@action = 'true'">
                      <xsl:attribute name='class'>click</xsl:attribute>
                    </xsl:if>
                    <xsl:if test="@new = 'ye'">
                      <xsl:attribute name='css:text-decoration'>underline</xsl:attribute>
                      <xsl:attribute name='css:color'>#C50069</xsl:attribute>
                    </xsl:if>
                    <xsl:choose>
                      <xsl:when test="@action = 'true' and @root!='0'">
                        <xsl:text> - </xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:if test="@plus='1' and @root!='0'">
                          <xsl:text> + </xsl:text>
                        </xsl:if>
                        <xsl:if test="@plus='0' and @root!='0'">
                          <xsl:text> - </xsl:text>
                       </xsl:if>
                    </xsl:otherwise>
                  </xsl:choose>
                  <xsl:value-of select="@name"/>
                  </xsl:element>
                  <xsl:call-template name="k_object"/>
                </li>
              </xsl:if>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:for-each>
      </ul>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>

