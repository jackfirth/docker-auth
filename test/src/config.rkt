#lang typed/racket/base

(require envy)

(define/provide-environment
  auth-service-domain
  backend-service-domain
  test-jwt)
