<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
     <xsl:template name="form">
         <xsl:element name="form">
            <xsl:attribute name='action'><xsl:value-of select='/r/data/form/@action'/></xsl:attribute>
            <xsl:attribute name='method'><xsl:value-of select='/r/data/form/@method'/></xsl:attribute>
             <table>
              <xsl:for-each select="/R/data/form/inp">
                <tr><td><xsl:value-of select="@name"/>
                    </td>
                    <td>
                      <xsl:choose>
                      <xsl:when test="@id = 'password'">
                        <xsl:element name='input'>
                          <xsl:attribute name='name'><xsl:value-of select="@id"/><xsl:value-of select="@id_inp"/></xsl:attribute>
                          <xsl:attribute name='id'>passwd<xsl:value-of select="@id_inp"/></xsl:attribute>
                          <xsl:attribute name='type'>password</xsl:attribute>
                        </xsl:element>
                      </xsl:when>
                      <xsl:when test="@id = 'address' or @id = 'phones'">
                        <xsl:element name='textarea'>
                          <xsl:attribute name='name'><xsl:value-of select="@id"/></xsl:attribute>
                          <xsl:attribute name='rows'>5</xsl:attribute>
                          <xsl:attribute name='cols'>40</xsl:attribute>
                          <xsl:value-of select="@default"/>
                        </xsl:element>
                      </xsl:when>
                      <xsl:otherwise>
                      <xsl:element name='input'>
                        <xsl:attribute name='name'><xsl:value-of select="@id"/></xsl:attribute>
                        <xsl:attribute name='type'>text</xsl:attribute>
                        <xsl:attribute name='value'><xsl:value-of select="@default"/></xsl:attribute>
                      </xsl:element>
                    </xsl:otherwise>
                  </xsl:choose>
                 </td>
               </tr>
              </xsl:for-each>
              <xsl:for-each select="/R/data/form/select">
                <tr><td><xsl:value-of select="@name"/>
                  </td>
                  <td>
                    <xsl:element name='select'>
                      <xsl:attribute name='name'><xsl:value-of select="@id"/></xsl:attribute>
                      <xsl:for-each select="./option">
                          <xsl:element name='option'>
                            <xsl:attribute name='value'><xsl:value-of select="@name"/></xsl:attribute>
                            <xsl:value-of select="@value"/>
                          </xsl:element>
                        </xsl:for-each>
                    </xsl:element>
                  </td></tr>
              </xsl:for-each>
              <xsl:if test='/R/data/register'>
               <tr><td colspan='2'> Введите код, изображенный на картинке: </td></tr>
               <tr><td>
                   <xsl:element name='img'>
                     <xsl:attribute name='src'>/captcha?id=<xsl:value-of select="/R/data/register/@link"/></xsl:attribute>
                   </xsl:element>
                   </td>
                 <td>
                   <input type="text" name="captcha" size="10"/>
                   <xsl:element name='input'>
                    <xsl:attribute name='name'>public</xsl:attribute>
                    <xsl:attribute name='type'>hidden</xsl:attribute>
                    <xsl:attribute name='value'><xsl:value-of select="/R/data/register/@link"/></xsl:attribute>
                   </xsl:element>
                  </td></tr>
                </xsl:if>
                <tr><td colspan='2'><input type='submit' value='Зарегистрироваться'/></td></tr>
            </table>
          </xsl:element>
      </xsl:template>
</xsl:stylesheet>
