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
      [% path_collection %]
    ],
    fallback: false,
  }
}

export function getStaticProps(context) {
  switch (context.params.routes.join('/')) {
    [% template_collection %]

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
