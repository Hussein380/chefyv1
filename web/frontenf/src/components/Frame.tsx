import { FunctionComponent } from "react";
import styles from "./Frame.module.css";

export type FrameType = {
  className?: string;
};

const Frame: FunctionComponent<FrameType> = ({ className = "" }) => {
  return (
    <section className={[styles.frame, className].join(" ")}>
      <div className={styles.frame1}>
        <div className={styles.frameInner}>
          <div className={styles.frameParent}>
            <div className={styles.subtractParent}>
              <img className={styles.subtractIcon} alt="" src="/subtract.svg" />
              <div className={styles.frameChild} />
            </div>
            <div className={styles.frameWrapper}>
              <div className={styles.rectangleParent}>
                <div className={styles.frameItem} />
                <div className={styles.rectangleDiv} />
                <div className={styles.frameChild1} />
              </div>
            </div>
          </div>
        </div>
        <img className={styles.frameIcon} alt="" src="/frame-8.svg" />
      </div>
      <div className={styles.frame2}>
        <div className={styles.frame3}>
          <img className={styles.frameIcon1} alt="" src="/frame-9.svg" />
          <div className={styles.column}>
            <div className={styles.content}>
              <div className={styles.row}>
                <img
                  className={styles.subtractIcon1}
                  alt=""
                  src="/subtract.svg"
                />
                <div className={styles.circle} />
              </div>
              <div className={styles.content1}>
                <div className={styles.actions}>
                  <div className={styles.button} />
                  <div className={styles.buttonSecondary} />
                  <div className={styles.buttonTertiary} />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className={styles.frame4}>
          <img className={styles.frameIcon2} alt="" src="/frame-10.svg" />
          <div className={styles.frame5}>
            <div className={styles.column1}>
              <div className={styles.content2}>
                <div className={styles.row1}>
                  <img
                    className={styles.subtractIcon2}
                    alt=""
                    src="/subtract.svg"
                  />
                  <div className={styles.circle1} />
                </div>
                <div className={styles.content3}>
                  <div className={styles.actions1}>
                    <div className={styles.button1} />
                    <div className={styles.buttonSecondary1} />
                    <div className={styles.buttonTertiary1} />
                  </div>
                </div>
              </div>
            </div>
            <img className={styles.columnIcon} alt="" src="/frame-11.svg" />
          </div>
          <div className={styles.frame6}>
            <div className={styles.row2}>
              <div className={styles.column2}>
                <div className={styles.content4}>
                  <div className={styles.row3}>
                    <img
                      className={styles.subtractIcon3}
                      alt=""
                      src="/subtract.svg"
                    />
                    <div className={styles.circle2} />
                  </div>
                  <div className={styles.content5}>
                    <div className={styles.actions2}>
                      <div className={styles.button2} />
                      <div className={styles.buttonSecondary2} />
                      <div className={styles.buttonTertiary2} />
                    </div>
                  </div>
                </div>
              </div>
              <img className={styles.columnIcon1} alt="" src="/frame-12.svg" />
            </div>
            <img
              className={styles.columnIcon2}
              loading="lazy"
              alt=""
              src="/frame-13.svg"
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default Frame;
