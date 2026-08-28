package io.github.crustack.slf4j.callerinfo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class SealedImpl implements SealedClass {

  private final Logger log = LoggerFactory.getLogger(SealedImpl.class);

  @Override
  public void foo() {
    log.info("foo");
  }
}
