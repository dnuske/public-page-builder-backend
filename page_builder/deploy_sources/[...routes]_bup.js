import { HTMLRenderer } from '@react-page/editor/lib/renderer/HTMLRenderer';
import Head from 'next/head';

import Title from '../cells/Title';
import Text from '../cells/Text';
import Container from '../cells/Section';
import Image from '../cells/Image';
import BackgroundImage from '../cells/BackgroundImage';
import NavBar from '../cells/NavBar';
import Background from '@react-page/plugins-background';
import Button from '../cells/Button';
import CustomHtmlSnippet from '../cells/CustomHtmlSnippet';

import { ComposeWithStyles } from '../cells/ControlComponents/StylingControl';
import { ComposeWithResponsiveControl } from '../cells/ControlComponents/ResponsiveControls';

export default function CustomRoute(props) {

  const cells = ComposeWithResponsiveControl(
    ComposeWithStyles(
      [
        Title(),
        Text(),
        BackgroundImage(),
        Container(),
        Image(),
        NavBar(),
        Background(),
        Button(),
        CustomHtmlSnippet()
      ]));

  return (
    <>
      <Head>
        <title>{props.title}</title>
        {/* Agregar items de head aquí */}
      </Head>
      <HTMLRenderer cellPlugins={cells} value={props.value} readOnly={true} />
    </>
  )
}

export function getStaticPaths() {
  return {
    paths: [
      { params: { routes: "home" } },
      { params: { routes: "about" } },
    ],
    fallback: false,
  }
}

export function getStaticProps(context) {
  switch (context.params.routes) {
    case "home":
      return {
        props: {
          title: "Blank | No content",
          value: {}
        }
      }
    case "about":
      return {
        props: {
          title: "About us",
          value: { "version": 1, "rows": [{ "id": "izfphh", "cells": [{ "id": "c064ge", "size": 12, "plugin": { "id": "backgroundImage", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "" }, "minHeight": "100vh", "imageUrl": "https://images.squarespace-cdn.com/content/v1/5ce82b63338ade0001773744/1560194358763-0FSEP70XI34IL8XXZEQQ/ke17ZwdGBToddI8pDm48kOxLRGAfd8DHyn-VO-OS79h7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0s0XaMNjCqAzRibjnE_wBlnKv1yxoTk5msUVUpzS-jwidPkl-46T667XTMzLYTMBnw/pickle-perfection-v1.jpg", "backgroundRepeat": "no-repeat", "backgroundPosition": "center", "backgroundSize": "cover" } }, "rows": [{ "id": "54a6o6", "cells": [{ "id": "kgn17s", "size": 4, "plugin": { "id": "navBar", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "backgroundColor": "", "padding": "45px 0 0 45px", "fontSize": "18px" }, "items": [{ "id": 1, "label": "Shop", "link": "https://insert.link", "active": false }, { "id": 2, "label": "Our Story", "link": "https://insert.link", "active": false }, { "id": 3, "label": "Blog", "link": "https://insert.link", "active": false }], "itemStyles": { "padding": "20px 30px 0 0", "color": "white", "backgroundColor": "" }, "hoverStyles": { "color": "green", "backgroundColor": "" }, "activeStyles": { "color": "black", "backgroundColor": "" }, "flexOptions": { "flexDirection": "row", "alignItems": "flex-end" } } }, "rows": [], "inline": null }, { "id": "xn8wav", "size": 4, "plugin": { "id": "titleCell", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "white", "padding": "48px 0 10px 0", "backgroundColor": "", "fontSize": "24px" }, "title": "Hester", "alignment": "center", "tag": "h2" } }, "rows": [], "inline": null }, { "id": "9jyjs3", "size": 4, "plugin": { "id": "textCell", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "white", "padding": "55px", "backgroundColor": "" }, "text": "Login | Cart", "alignment": "right" } }, "rows": [], "inline": null }] }, { "id": "lmla82", "cells": [{ "id": "qaw1db", "size": 12, "plugin": { "id": "titleCell", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "white", "padding": "350px 0 40px 0", "backgroundColor": "", "fontSize": "46px" }, "title": "Pickle Perfection", "alignment": "center", "tag": "h2" } }, "rows": [], "inline": null }] }, { "id": "mb32tn", "cells": [{ "id": "qyjok0", "size": 12, "plugin": { "id": "buttonComponent" }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "margin": "auto", "fontSize": "24px", "padding": "10px", "color": "white", "backgroundColor": "", "border": "none" }, "text": "Shop Now", "innerStyles": { "color": "pink", "backgroundColor": "white", "padding": "15px 30px" }, "hoverStyles": { "color": "white", "backgroundColor": "black" }, "hover": false } }, "rows": [], "inline": null }] }], "inline": null }] }, { "id": "y3vapl", "cells": [{ "id": "hkz5mo", "size": 12, "plugin": { "id": "titleCell", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "105px 0 30px 0", "backgroundColor": "", "fontSize": "26px" }, "title": "Only the Highest Quality Ingredients", "alignment": "center", "tag": "h2" } }, "rows": [], "inline": null }] }, { "id": "1cagzj", "cells": [{ "id": "k9wigd", "size": 12, "plugin": { "id": "textCell", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "0 0 200px 0", "backgroundColor": "", "fontSize": "20px", "fontWeight": "100" }, "text": "In fact, we grow most of them ourselves on our 17-acre farm!\n\n", "alignment": "center" } }, "rows": [], "inline": null }] }, { "id": "tq87y1", "cells": [{ "id": "gz0ovl", "size": 12, "plugin": { "id": "container", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "" }, "minHeight": "500px", "maxWidth": "1400px" } }, "rows": [{ "id": "6d0cw6", "cells": [{ "id": "82im34", "size": 4, "plugin": { "id": "image", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "" }, "imageUrl": "https://images.squarespace-cdn.com/content/v1/5ce82b63338ade0001773744/1559253805745-IUOL4DLCPMQN7BMAY4OQ/ke17ZwdGBToddI8pDm48kMtiXMEMZ8ID8MVhA-T_Qc9Zw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZamWLI2zvYWH8K3-s_4yszcp2ryTI0HqTOaaUohrI8PIfy9uRsqnknGrsPwiW8VdnsJxMq6FvgYbxptNsO-6IOIKMshLAGzx4R3EDFOm1kBS/download+%287%29.jpeg?format=500w", "height": "450px", "alignment": "center" } }, "rows": [], "inline": null }, { "id": "20qlrz", "size": 4, "plugin": { "id": "image", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "" }, "imageUrl": "https://images.squarespace-cdn.com/content/v1/5ce82b63338ade0001773744/1559254414057-BT9LBEFTBQBMJPA9CMVZ/ke17ZwdGBToddI8pDm48kMtiXMEMZ8ID8MVhA-T_Qc9Zw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZamWLI2zvYWH8K3-s_4yszcp2ryTI0HqTOaaUohrI8PIfy9uRsqnknGrsPwiW8VdnsJxMq6FvgYbxptNsO-6IOIKMshLAGzx4R3EDFOm1kBS/download+%282%29.jpeg?format=500w", "height": "450px", "alignment": "center" } }, "rows": [], "inline": null }, { "id": "ry90mb", "size": 4, "plugin": { "id": "image", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "" }, "imageUrl": "https://images.squarespace-cdn.com/content/v1/5ce82b63338ade0001773744/1559253861275-XR8S53GVN47EFCIQQ8UQ/ke17ZwdGBToddI8pDm48kMtiXMEMZ8ID8MVhA-T_Qc9Zw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZamWLI2zvYWH8K3-s_4yszcp2ryTI0HqTOaaUohrI8PIfy9uRsqnknGrsPwiW8VdnsJxMq6FvgYbxptNsO-6IOIKMshLAGzx4R3EDFOm1kBS/download+%286%29.jpeg?format=500w", "height": "450px", "alignment": "center" } }, "rows": [], "inline": null }] }], "inline": null }] }, { "id": "wsoppt", "cells": [{ "id": "c71qg8", "size": 12, "plugin": { "id": "buttonComponent" }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "margin": "auto", "fontSize": "20px", "padding": "100px" }, "text": "Shop Now", "innerStyles": { "color": "white", "backgroundColor": "pink", "padding": "20px 30px" }, "hoverStyles": { "color": "white", "backgroundColor": "black" }, "hover": false } }, "rows": [], "inline": null }] }, { "id": "c03d02", "cells": [{ "id": "qpoagx", "size": 12, "plugin": { "id": "backgroundImage", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "" }, "minHeight": "100vh", "imageUrl": "https://images.squarespace-cdn.com/content/v1/5ce82b63338ade0001773744/1559153723232-1DM5OCLN1FPII8S0S6I5/ke17ZwdGBToddI8pDm48kLkXF2pIyv_F2eUT9F60jBl7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0iyqMbMesKd95J-X4EagrgU9L3Sa3U8cogeb0tjXbfawd0urKshkc5MgdBeJmALQKw/pink-image.jpg", "backgroundRepeat": "no-repeat", "backgroundPosition": "center", "backgroundSize": "cover" } }, "rows": [], "inline": null }] }, { "id": "j48tcz", "cells": [{ "id": "zy5zn7", "size": 12, "plugin": { "id": "titleCell", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "100px 0 20px 0", "backgroundColor": "", "fontSize": "32px" }, "title": "What’s the Dill?", "alignment": "center", "tag": "h2" } }, "rows": [], "inline": null }] }, { "id": "oigriw", "cells": [{ "id": "s4etpv", "size": 12, "plugin": { "id": "textCell", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "", "fontSize": "22px", "fontWeight": "100" }, "text": "Sign up with your email address to receive news and updates.\n\n", "alignment": "center" } }, "rows": [], "inline": null }] }, { "id": "fu74gh", "cells": [{ "id": "2voucr", "size": 12, "plugin": { "id": "buttonComponent" }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "margin": "auto", "fontSize": "20px", "padding": "100px" }, "text": "Suscribe", "innerStyles": { "color": "white", "backgroundColor": "pink", "padding": "20px 30px" }, "hoverStyles": { "color": "white", "backgroundColor": "black" }, "hover": false } }, "rows": [], "inline": null }] }, { "id": "ljegte", "cells": [{ "id": "329ta3", "size": 12, "plugin": { "id": "container", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "" }, "minHeight": "500px", "maxWidth": "1450px" } }, "rows": [{ "id": "od5hqe", "cells": [{ "id": "pai57u", "size": 4, "plugin": { "id": "image", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "" }, "imageUrl": "https://images.squarespace-cdn.com/content/v1/5ce82b63338ade0001773744/1585672165410-UV0ZPANAANU3C1TWWIIJ/ke17ZwdGBToddI8pDm48kMtiXMEMZ8ID8MVhA-T_Qc9Zw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZamWLI2zvYWH8K3-s_4yszcp2ryTI0HqTOaaUohrI8PIfy9uRsqnknGrsPwiW8VdnsJxMq6FvgYbxptNsO-6IOIKMshLAGzx4R3EDFOm1kBS/pickels.jpeg?format=500w", "height": "433px", "alignment": "center" } }, "rows": [], "inline": null }, { "id": "u6vxhg", "size": 4, "plugin": { "id": "image", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "" }, "imageUrl": "https://images.squarespace-cdn.com/content/v1/5ce82b63338ade0001773744/1585672165647-FHINUJX0SLBWU9XH77XJ/ke17ZwdGBToddI8pDm48kMtiXMEMZ8ID8MVhA-T_Qc9Zw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZamWLI2zvYWH8K3-s_4yszcp2ryTI0HqTOaaUohrI8PIfy9uRsqnknGrsPwiW8VdnsJxMq6FvgYbxptNsO-6IOIKMshLAGzx4R3EDFOm1kBS/hot-pepper.jpeg?format=500w", "height": "433px", "alignment": "center" } }, "rows": [], "inline": null }, { "id": "01zwqj", "size": 4, "plugin": { "id": "image", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "" }, "imageUrl": "https://images.squarespace-cdn.com/content/v1/5ce82b63338ade0001773744/1585672165290-B0RLEMS59MGCBBHL4Z8B/ke17ZwdGBToddI8pDm48kMtiXMEMZ8ID8MVhA-T_Qc9Zw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZamWLI2zvYWH8K3-s_4yszcp2ryTI0HqTOaaUohrI8PIfy9uRsqnknGrsPwiW8VdnsJxMq6FvgYbxptNsO-6IOIKMshLAGzx4R3EDFOm1kBS/cabbage.jpeg?format=500w", "height": "433px", "alignment": "center" } }, "rows": [], "inline": null }] }], "inline": null }] }, { "id": "t7rfpe", "cells": [{ "id": "njve53", "size": 12, "plugin": { "id": "container", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "white", "padding": "", "backgroundColor": "#df7c6d" }, "minHeight": "350px", "maxWidth": "1400px" } }, "rows": [{ "id": "wxt968", "cells": [{ "id": "9vtdu8", "size": 12, "plugin": { "id": "titleCell", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "white", "padding": "70px 0 40px 0", "backgroundColor": "" }, "title": "Hester", "alignment": "left", "tag": "h2" } }, "rows": [], "inline": null }] }, { "id": "j9zq0x", "cells": [{ "id": "w4uabt", "size": 12, "plugin": { "id": "textCell", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "" }, "text": "123 Demo Street\n", "alignment": "left" } }, "rows": [], "inline": null }] }, { "id": "4io7kf", "cells": [{ "id": "mf17ah", "size": 12, "plugin": { "id": "textCell", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "" }, "text": "New York, NY 10000\n", "alignment": "left" } }, "rows": [], "inline": null }] }, { "id": "smnsis", "cells": [{ "id": "qkb1nj", "size": 12, "plugin": { "id": "textCell", "version": 1 }, "dataI18n": { "default": { "visibility": { "desktop": true, "mobile": false }, "styles": { "color": "", "padding": "", "backgroundColor": "" }, "text": "(555) 555-555", "alignment": "left" } }, "rows": [], "inline": null }] }], "inline": null }] }] }
        }
      }
    default:
      return {
        props: {
          title: "Blank | No content",
          value: {}
        }
      }
  }
  return {}
}
