import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './styles.module.css';

const features = [
  {
    title: 'Easy to Use',
    imageUrl: 'img/undraw_docusaurus_mountain.svg',
    description: (
      <>
        pnguin was designed from the ground up to actually <b>work</b>. No complicated functions,
        no confusing approaches to data manipulation. Access, read, and edit datasets in seconds.
      </>
    ),
  },
  {
    title: 'Two Axes > One Axis',
    imageUrl: 'img/undraw_docusaurus_tree.svg',
    description: (
      <>
        Columnar DataFrames are annoying. pnguin enables bi-axial DataFrames,
        allowing for both column and row based data access. It's fast, and it's convinient.
      </>
    ),
  },
  {
    title: 'Remote DataFrames',
    imageUrl: 'img/undraw_docusaurus_react.svg',
    description: (
      <>
        RemoteFrames allow you to stream both SQL and BigQuery datasets to your notebook.
        View and query without actually loading data in memory, and convert to a DataFrame to edit.
      </>
    ),
  },
];

function Feature({imageUrl, title, description}) {
  const imgUrl = useBaseUrl(imageUrl);
  return (
    <div className={clsx('col col--4', styles.feature)}>
      {imgUrl && (
        <div className="text--center">
          <img className={styles.featureImage} src={imgUrl} alt={title} />
        </div>
      )}
      <h3 style={{textAlign: "center"}}>{title}</h3>
      <p style={{textAlign: "center"}}>{description}</p>
    </div>
  );
}

function Home() {
  const context = useDocusaurusContext();
  const {siteConfig = {}} = context;
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <header className={clsx('hero hero--primary', styles.heroBanner)}>
        <div className="container">
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.buttons}>
            <Link
              className={clsx(
                'button button--outline button--secondary button--lg',
                styles.getStarted,
              )}
              to={useBaseUrl('docs/')}>
              Get Started
            </Link>
          </div>
        </div>
      </header>
      <main>
        {features && features.length > 0 && (
          <section className={styles.features}>
            <div className="container">
              <div className="row">
                {features.map((props, idx) => (
                  <Feature key={idx} {...props} />
                ))}
              </div>
            </div>
          </section>
        )}
      </main>
    </Layout>
  );
}

export default Home;
